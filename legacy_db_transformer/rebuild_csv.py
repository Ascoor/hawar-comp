#!/usr/bin/env python3
"""Rebuild legacy CSV files to match Laravel migration structure.

This script combines all files matching ``members_with_header_part*.csv``
from the ``sqls/csv`` folder and writes ``members_restructured.csv`` with
columns corresponding to the ``members`` table defined in the Laravel
migrations.
"""

import csv
from pathlib import Path

PARTS_DIR = Path(__file__).parent / "sqls" / "csv"
OUTPUT_FILE = Path(__file__).parent / "members_restructured.csv"

LEGACY_HEADER = [
    "index",
    "Mem_ID",
    "Mem_Name",
    "Mem_Code",
    "Mem_BOD",
    "Mem_NID",
    "Mem_GraduationGrade",
    "Mem_ParentMember",
    "Mem_Sex",
    "Mem_JobCategory",
    "Mem_Job",
    "Mem_MembershipType",
    "Mem_Relegion",
    "Mem_Address",
    "Mem_JoinDate",
    "Mem_Class",
    "Mem_HomePhone",
    "Mem_Mobile",
    "Mem_Receiver",
    "Mem_WorkPhone",
    "Mem_Photo",
    "Mem_Notes",
    "Mem_LastPayedFees",
    "Mem_Status",
    "MemCard_MemberName",
    "MemCard_MemberJobTitle",
    "Mem_GraduationDesc",
    "Mem_Notes_2",
    "Mem_Notes_3",
    "Mem_Notes_4",
    "Mem_Relation",
    "Mem_BoardDecision_Date",
    "Mem_BoardDecision_Number",
    "created_at",
    "updated_at",
]

OUTPUT_HEADER = [
    "id",
    "Mem_Name",
    "Mem_Code",
    "Mem_BOD",
    "Mem_NID",
    "Mem_GraduationGrade",
    "Mem_ParentMember",
    "Mem_Sex",
    "Mem_JobCategory",
    "Mem_Job",
    "Mem_MembershipType",
    "Mem_Relegion",
    "Mem_Address",
    "Mem_JoinDate",
    "Mem_Class",
    "Mem_HomePhone",
    "Mem_Mobile",
    "Mem_Receiver",
    "Mem_WorkPhone",
    "Mem_Photo",
    "Mem_Notes",
    "Mem_LastPayedFees",
    "Mem_Status",
    "MemCard_MemberName",
    "MemCard_MemberJobTitle",
    "Mem_GraduationDesc",
    "Mem_Notes_2",
    "Mem_Notes_3",
    "Mem_Notes_4",
    "Mem_Relation",
    "Mem_BoardDecision_Date",
    "Mem_BoardDecision_Number",
    "created_at",
    "updated_at",
    "category_id",
    "relation_id",
    "status_id",
    "family_id",
]

def iter_rows():
    for path in sorted(PARTS_DIR.glob("members_with_header_part*.csv")):
        with path.open("r", newline="", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            next(reader, None)  # skip header
            for row in reader:
                if not row:
                    continue
                data = dict(zip(LEGACY_HEADER, row))
                yield {
                    "id": data.get("Mem_ID"),
                    "Mem_Name": data.get("Mem_Name"),
                    "Mem_Code": data.get("Mem_Code"),
                    "Mem_BOD": data.get("Mem_BOD"),
                    "Mem_NID": data.get("Mem_NID"),
                    "Mem_GraduationGrade": data.get("Mem_GraduationGrade"),
                    "Mem_ParentMember": data.get("Mem_ParentMember"),
                    "Mem_Sex": data.get("Mem_Sex"),
                    "Mem_JobCategory": data.get("Mem_JobCategory"),
                    "Mem_Job": data.get("Mem_Job"),
                    "Mem_MembershipType": data.get("Mem_MembershipType"),
                    "Mem_Relegion": data.get("Mem_Relegion"),
                    "Mem_Address": data.get("Mem_Address"),
                    "Mem_JoinDate": data.get("Mem_JoinDate"),
                    "Mem_Class": data.get("Mem_Class"),
                    "Mem_HomePhone": data.get("Mem_HomePhone"),
                    "Mem_Mobile": data.get("Mem_Mobile"),
                    "Mem_Receiver": data.get("Mem_Receiver"),
                    "Mem_WorkPhone": data.get("Mem_WorkPhone"),
                    "Mem_Photo": data.get("Mem_Photo"),
                    "Mem_Notes": data.get("Mem_Notes"),
                    "Mem_LastPayedFees": data.get("Mem_LastPayedFees"),
                    "Mem_Status": data.get("Mem_Status"),
                    "MemCard_MemberName": data.get("MemCard_MemberName"),
                    "MemCard_MemberJobTitle": data.get("MemCard_MemberJobTitle"),
                    "Mem_GraduationDesc": data.get("Mem_GraduationDesc"),
                    "Mem_Notes_2": data.get("Mem_Notes_2"),
                    "Mem_Notes_3": data.get("Mem_Notes_3"),
                    "Mem_Notes_4": data.get("Mem_Notes_4"),
                    "Mem_Relation": data.get("Mem_Relation"),
                    "Mem_BoardDecision_Date": data.get("Mem_BoardDecision_Date"),
                    "Mem_BoardDecision_Number": data.get("Mem_BoardDecision_Number"),
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at"),
                    "category_id": "",
                    "relation_id": "",
                    "status_id": "",
                    "family_id": "",
                }

def main():
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_HEADER)
        writer.writeheader()
        for row in iter_rows():
            writer.writerow(row)

if __name__ == "__main__":
    main()
