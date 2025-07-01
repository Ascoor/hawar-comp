# -*- coding: utf-8 -*-
"""Normalize membership CSV for import.

This script reads a legacy CSV file with mixed Arabic/English headers,
standardizes field names, cleans categorical columns, deduplicates
records and resolves parent member IDs using fuzzy matching.
The result is written to stdout as UTF-8 CSV suitable for import
into the Laravel membership schema.
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

try:
    from fuzzywuzzy import process
except Exception:  # pragma: no cover - optional import
    process = None  # type: ignore


# synonyms for expected columns in the legacy file
COLUMN_SYNONYMS = {
    "id": ["id", "ID", "Mem_ID", "عضويةID"],
    "name": ["name", "full_name", "Mem_Name", "الاسم"],
    "code": ["code", "member_code", "Mem_Code", "كود"],
    "national_id": ["national_id", "nid", "Mem_NID", "الرقم القومي"],
    "birth_date": ["birth_date", "dob", "Mem_BOD", "تاريخ الميلاد"],
    "gender": ["gender", "Mem_Sex", "النوع"],
    "category": ["category", "membership_type", "Mem_MembershipType", "نوع العضوية"],
    "relation_type": ["relation", "relation_type", "Mem_Relation", "صلة القرابة"],
    "status": ["status", "Mem_Status", "حالة العضوية"],
    "parent_name": ["parent_member", "Mem_ParentMember", "اسم المشترك الرئيسي"],
    "parent_member_id": ["parent_member_id"],
    "join_date": ["join_date", "Mem_JoinDate", "تاريخ الاشتراك"],
    "address": ["address", "Mem_Address", "العنوان"],
    "phone": ["phone", "Mem_HomePhone", "التليفون"],
    "mobile": ["mobile", "Mem_Mobile", "الموبايل"],
    "notes": ["notes", "Mem_Notes", "ملاحظات"],
    "last_paid_fee": ["last_paid_fee", "Mem_LastPayedFees", "آخر سداد"],
}

GENDER_MAP = {
    "ذكر": "M",
    "أنثى": "F",
    "M": "M",
    "F": "F",
}

CATEGORY_MAP = {
    "عضو عامل": "Primary",
    "عضو تابع": "Family",
    "عضو مؤسس": "Honorary",
}

STATUS_MAP = {
    "مفعل": "Active",
    "موقوف": "Suspended",
    "ملغي": "Inactive",
}

RELATION_MAP = {
    "زوج": "Spouse",
    "زوجة": "Spouse",
    "ابن": "Child",
    "إبن": "Child",
    "ابنة": "Child",
    "إبنة": "Child",
}


def parse_date(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def find_columns(header):
    mapping = {}
    for std, aliases in COLUMN_SYNONYMS.items():
        for col in header:
            if col.strip() in aliases:
                mapping[std] = col
                break
    return mapping


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = find_columns(reader.fieldnames or [])
        for row in reader:
            yield {{k: row.get(v, "") for k, v in cols.items()}}


def normalize_row(row: dict) -> dict:
    return {
        "id": row.get("id") or None,
        "name": row.get("name") or None,
        "code": row.get("code") or None,
        "national_id": row.get("national_id") or None,
        "birth_date": parse_date(row.get("birth_date", "")),
        "gender": GENDER_MAP.get(row.get("gender", "").strip(), row.get("gender")),
        "category": CATEGORY_MAP.get(row.get("category", "").strip(), row.get("category")),
        "relation_type": RELATION_MAP.get(row.get("relation_type", "").strip(), row.get("relation_type")),
        "status": STATUS_MAP.get(row.get("status", "").strip(), row.get("status")),
        "parent_member_id": row.get("parent_member_id") or None,
        "parent_name": row.get("parent_name") or None,
        "join_date": parse_date(row.get("join_date", "")),
        "address": row.get("address") or None,
        "phone": row.get("phone") or None,
        "mobile": row.get("mobile") or None,
        "notes": row.get("notes") or None,
        "last_paid_fee": row.get("last_paid_fee") or None,
    }


def deduplicate(rows):
    seen = set()
    unique = []
    for r in rows:
        key = (r.get("code"), r.get("national_id"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    return unique


def resolve_parents(rows: list[dict]):
    if process is None:
        return rows
    mains = {r["name"]: r["id"] for r in rows if not r.get("relation_type") or r["relation_type"] == "Primary"}
    for r in rows:
        if r.get("relation_type") and r["relation_type"] != "Primary" and not r.get("parent_member_id") and r.get("parent_name"):
            match = process.extractOne(r["parent_name"], list(mains.keys()))
            if match and match[1] >= 80:
                r["parent_member_id"] = mains[match[0]]
    return rows


def write_csv(rows):
    fieldnames = [
        "id",
        "name",
        "code",
        "national_id",
        "birth_date",
        "gender",
        "category",
        "relation_type",
        "status",
        "parent_member_id",
        "join_date",
        "address",
        "phone",
        "mobile",
        "notes",
        "last_paid_fee",
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)


def main(path: Path):
    rows = [normalize_row(r) for r in read_rows(path)]
    rows = deduplicate(rows)
    rows = resolve_parents(rows)
    write_csv(rows)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python normalize_membership_csv.py <file.csv>", file=sys.stderr)
        sys.exit(1)
    main(Path(sys.argv[1]))
