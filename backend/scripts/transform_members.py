import csv
from datetime import datetime
from pathlib import Path

# Mapping dictionaries for cleaning legacy data
GENDER_MAP = {
    'ذكر': 'M',
    'أنثى': 'F',
}

STATUS_MAP = {
    'مفعل': 'Active',
    'موقوف': 'Suspended',
    'ملغي': 'Expired',
}

RELATION_MAP = {
    'زوج': 'Spouse',
    'زوجة': 'Spouse',
    'ابن': 'Child',
    'إبن': 'Child',
    'ابنة': 'Child',
    'إبنة': 'Child',
    'والد': 'Parent',
    'والدة': 'Parent',
}

# Membership category mapping based on legacy Arabic text
CATEGORY_MAP = {
    'عضو عامل': 'Primary',
    'عضو تابع': 'Family',
    'عضو مؤسس': 'Honorary',
}

def parse_date(value: str):
    """Return date in YYYY-MM-DD or None."""
    value = value.strip()
    for fmt in ('%d-%m-%Y', '%Y-%m-%d'):  # legacy files use both styles
        try:
            return datetime.strptime(value, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None


def parse_sql(sql_path: Path):
    """Yield rows from a legacy .sql dump containing INSERT statements."""
    import re

    text = sql_path.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(r"INSERT\s+INTO\s+`?\w+`?\s*\(([^)]*)\)\s*VALUES\s*(.*?);", re.DOTALL | re.IGNORECASE)
    row_pattern = re.compile(r"\((.*?)\)(?:,|$)", re.DOTALL)

    for cols_str, values_part in pattern.findall(text):
        columns = [c.strip("` ") for c in cols_str.split(',')]
        for row_txt in row_pattern.findall(values_part):
            values = next(csv.reader([row_txt], quotechar="'", skipinitialspace=True))
            yield dict(zip(columns, values))


def load_data(path: Path):
    """Return list of dicts from CSV or SQL file."""
    if path.suffix.lower() == ".sql":
        return list(parse_sql(path))
    with path.open(newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def deduplicate(rows):
    """Remove duplicate members by code or national id."""
    seen = set()
    unique = []
    for r in rows:
        key = (r.get('Mem_Code'), r.get('Mem_NID'))
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    return unique


def clean_row(row: dict) -> dict:
    """Clean and normalize a raw CSV row from legacy members."""
    return {
        'name': row.get('Mem_Name'),
        'member_code': row.get('Mem_Code'),
        'national_id': row.get('Mem_NID') or None,
        'birth_date': parse_date(row.get('Mem_BOD', '')),
        'join_date': parse_date(row.get('Mem_JoinDate', '')),
        'gender': GENDER_MAP.get(row.get('Mem_Sex', '').strip()),
        'status': STATUS_MAP.get(row.get('Mem_Status', '').strip()),
        'relation': RELATION_MAP.get(row.get('Mem_Relation', '').strip()),
        'category': CATEGORY_MAP.get(row.get('Mem_MembershipType', '').strip()),
        'fee_year': row.get('Fee_Year'),
        'fee_amount': row.get('Fee_Amount'),
    }


def transform(path: Path):
    """Return cleaned member rows from *path* (CSV or SQL)."""
    raw_rows = load_data(path)
    raw_rows = deduplicate(raw_rows)
    cleaned = [clean_row(r) for r in raw_rows]
    return cleaned

if __name__ == '__main__':
    import json, sys
    import argparse

    parser = argparse.ArgumentParser(description="Clean legacy member CSV or SQL data")
    parser.add_argument("file", help="Path to legacy file (.csv or .sql)")
    parser.add_argument("--csv", action="store_true", help="Output CSV instead of JSON")
    args = parser.parse_args()

    path = Path(args.file)
    records = transform(path)

    if args.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    else:
        json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
