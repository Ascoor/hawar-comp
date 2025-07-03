# -*- coding: utf-8 -*-
"""Import members and users from legacy CSV.

This script reads the members CSV exported from the legacy system,
cleans the values and inserts records into the ``users`` and
``member_details`` tables of the Laravel database.
"""

import csv
import hashlib
from datetime import datetime, date
from pathlib import Path

import mysql.connector

# Database configuration - edit as needed
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "laravel",
    "charset": "utf8mb4",
}

# Mapping dictionaries from Arabic text/codes to lookup IDs
CATEGORY_MAP = {
    "عضو عامل": 1,  # working_member
    "عضو تابع": 2,  # affiliate_member
    "عضو مؤسس": 3,  # founding_member
    "عضوية فخرية": 4,  # honorary_member
    "عضوية موسمية": 5,  # seasonal_member
    "عضوية مؤقتة": 5,
    "عضوية مؤقتة - تابع": 5,
    "عضو تابع - موسمية": 5,
}

STATUS_MAP = {
    "مفعل": 1,  # Active
    "مسقطة - مفصول": 2,  # Dropped
    "مسقطة - متوفي": 6,  # Deceased
    "": 1,
}

RELATION_MAP = {
    "": 1,   # Owner/default
    "73": 1,
    "74": 2,  # Husband
    "75": 3,  # Wife
    "76": 4,  # Son
    "77": 5,  # daughter
    "78": 4,
    "79": 5,
    "131": 4,
    "132": 5,
}

# Simple transliteration from Arabic to Latin characters
TRANSLIT = {
    "ا": "a", "أ": "a", "إ": "i", "آ": "a", "ب": "b", "ت": "t", "ث": "th",
    "ج": "j", "ح": "h", "خ": "kh", "د": "d", "ذ": "dh", "ر": "r",
    "ز": "z", "س": "s", "ش": "sh", "ص": "s", "ض": "d", "ط": "t",
    "ظ": "z", "ع": "a", "غ": "gh", "ف": "f", "ق": "q", "ك": "k",
    "ل": "l", "م": "m", "ن": "n", "ه": "h", "و": "w", "ي": "y",
    "ة": "a", "ى": "a", "ئ": "e", "ء": "a", "ؤ": "u",
}

def transliterate(text: str) -> str:
    result = []
    for ch in text:
        if ch == " ":
            result.append("-")
        else:
            result.append(TRANSLIT.get(ch, ch))
    slug = "".join(result)
    slug = slug.encode("ascii", "ignore").decode("ascii")
    slug = slug.lower()
    return slug

def parse_date(value: str) -> str | None:
    value = value.strip()
    if not value or value in {"-", "--"}:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def clean(val: str) -> str | None:
    if val is None:
        return None
    val = str(val).strip()
    if val in {"", "-", "--"}:
        return None
    return val

def calc_age(dob: str | None) -> str | None:
    if not dob:
        return None
    try:
        birth = datetime.strptime(dob, "%Y-%m-%d").date()
        today = date.today()
        return str(today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day)))
    except Exception:
        return None

def determine_family_id(row: dict, name_to_id: dict) -> str:
    parent = clean(row.get("Mem_ParentMember"))
    if parent:
        return parent
    is_main = str(row.get("Mem_IsMainMember", "")).strip()
    member_id = str(row.get("Mem_Code") or row.get("Mem_ID"))
    if is_main in {"-1.0", "1.0", "-1", "1"}:
        return member_id
    if is_main in {"0", "-0", "0.0"}:
        parent_name = clean(row.get("parentName"))
        if parent_name and parent_name in name_to_id:
            return name_to_id[parent_name]
    return member_id

def main(csv_path: Path) -> None:
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    name_to_id: dict[str, str] = {}

    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            member_id = str(clean(row.get("Mem_Code")) or clean(row.get("Mem_ID")) or "")
            if not member_id:
                continue
            name = clean(row.get("Mem_Name")) or ""
            family_id = determine_family_id(row, name_to_id)
            dob = parse_date(row.get("Mem_BOD", ""))
            age = calc_age(dob)
            gender = "male" if row.get("Gender") == "ذكر" else "female" if row.get("Gender") == "أنثى" else "others"

            # generate email and password
            slug = transliterate(name.split()[0]) if name else "user"
            email = f"{slug}-{member_id}@hawar.club"
            password_plain = f"hawar@{member_id}"
            password_hash = hashlib.sha256(password_plain.encode()).hexdigest()

            # insert user
            cur.execute(
                "INSERT INTO users (name, email, password, created_at, updated_at) "
                "VALUES (%s, %s, %s, NOW(), NOW())",
                (name, email, password_hash),
            )
            user_id = cur.lastrowid

            mem_data = (
                member_id,
                family_id,
                name,
                clean(row.get("Mem_NID")),
                user_id,
                gender,
                CATEGORY_MAP.get(row.get("MembershipType", "").strip(), 1),
                RELATION_MAP.get(row.get("Mem_Relation", "").strip(), 1),
                STATUS_MAP.get(row.get("Status", "").strip(), 1),
                clean(row.get("Mem_Mobile")),
                dob,
                email,
                clean(row.get("Mem_Address")),
                clean(row.get("Mem_City")),
                clean(row.get("Mem_State")),
                age,
                clean(row.get("Mem_Job")),
                clean(row.get("Relegion")),
                64,
                64,
                "renewed",
                None,
                None,
                None,
                clean(row.get("Mem_Notes")),
                clean(row.get("Mem_Notes_2")),
                clean(row.get("Mem_Notes_3")),
                clean(row.get("Mem_Notes_4")),
                parse_date(row.get("Mem_LastPayedFees", "")),
                parse_date(row.get("Mem_BoardDecision_Date", "")),
                clean(row.get("Mem_BoardDecision_Number")),
                clean(row.get("MemCard_MemberName")),
                clean(row.get("MemCard_MemberJobTitle")),
                clean(row.get("Mem_GraduationDesc")),
                clean(row.get("Mem_WorkPhone")),
                clean(row.get("Mem_HomePhone")),
                None,
                None,
                None,
                datetime.now(),
                datetime.now(),
            )

            cur.execute(
                """
                INSERT INTO member_details (
                    member_id, family_id, name, national_id, user_id, gender,
                    category_id, relation_id, status_id, phone, date_of_birth,
                    email, address, city, state, age, profession, religion,
                    country_id, nationality_id, renewal_status, postal_code,
                    face_book, twitter, note, note_2, note_3, note_4,
                    last_paid_fiscal_year, date_of_the_board_of_directors,
                    decision_number, memCard_MemberName, remarks,
                    mem_GraduationDesc, mem_WorkPhone, mem_HomePhone,
                    email_notifications, player, team_id, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                mem_data,
            )
            conn.commit()
            name_to_id[name] = member_id
    cur.close()
    conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python import_members_and_users.py <file.csv>")
        sys.exit(1)
    main(Path(sys.argv[1]))
