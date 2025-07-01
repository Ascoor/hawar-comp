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

def parse_date(value: str):
    """Return date in YYYY-MM-DD or None."""
    value = value.strip()
    for fmt in ('%d-%m-%Y', '%Y-%m-%d'):  # legacy files use both styles
        try:
            return datetime.strptime(value, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None


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
        'address': row.get('Mem_Address'),
        'mobile': row.get('Mem_Mobile'),
    }


def transform(csv_path: Path):
    with csv_path.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        cleaned = [clean_row(r) for r in reader]
    return cleaned

if __name__ == '__main__':
    import json, sys
    import argparse

    parser = argparse.ArgumentParser(description="Clean legacy member CSV data")
    parser.add_argument("file", help="Path to legacy CSV")
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
