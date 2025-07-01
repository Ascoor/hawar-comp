#!/usr/bin/env python
"""Convert SQL INSERT dumps into Laravel Seeder classes.

The script reads SQL files with INSERT statements and generates
corresponding Laravel seeders under the provided output directory.
It supports chunking large tables into multiple classes.
"""

import argparse
import logging
import math
import re
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional
import csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Regular expressions for parsing
INSERT_RE = re.compile(
    r"INSERT\s+INTO\s+`?(\w+)`?\s*(\(([^)]*)\))?\s+VALUES\s*(.*?);",
    re.IGNORECASE | re.DOTALL,
)
ROW_RE = re.compile(r"\((.*?)\)(?:,|$)", re.DOTALL)
CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+`?(\w+)`?\s*\((.*?)\);",
    re.IGNORECASE | re.DOTALL,
)


def parse_schema(text: str) -> Dict[str, List[str]]:
    """Return mapping of table name to column list from CREATE TABLE statements."""
    schema: Dict[str, List[str]] = {}
    for match in CREATE_TABLE_RE.finditer(text):
        table = match.group(1).lower()
        block = match.group(2)
        columns: List[str] = []
        for line in block.splitlines():
            line = line.strip().strip(",")
            if not line or line.upper().startswith("CONSTRAINT") or line.upper().startswith("PRIMARY KEY"):
                continue
            col = line.split()[0].strip("`")
            columns.append(col)
        schema[table] = columns
    return schema


def parse_row(text: str) -> List[Optional[str]]:
    """Parse a parenthesized row value list."""
    row = next(csv.reader(StringIO(text), quotechar="'", skipinitialspace=True))
    return [None if v.upper() == "NULL" else v for v in row]


def parse_inserts(text: str) -> Dict[str, Dict[str, List]]:
    """Extract inserts grouped by table."""
    data: Dict[str, Dict[str, List]] = {}
    for match in INSERT_RE.finditer(text):
        table = match.group(1).lower()
        columns_raw = match.group(3)
        columns = [c.strip("` ") for c in columns_raw.split(",")] if columns_raw else None
        values_part = match.group(4)
        rows = [parse_row(r) for r in ROW_RE.findall(values_part)]
        entry = data.setdefault(table, {"columns": columns, "rows": []})
        entry["rows"].extend(rows)
    return data


def php_value(value: Optional[str]) -> str:
    if value is None:
        return "null"
    if re.fullmatch(r"-?\d+(?:\.\d+)?", value):
        return value
    return "'" + value.replace("'", "\\'") + "'"


def camel_case(name: str) -> str:
    return "".join(word.capitalize() for word in re.split(r"_+", name))


def generate_seeders(data: Dict[str, Dict[str, List]], schema: Dict[str, List[str]], output_dir: Path, chunk: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for table, info in data.items():
        columns = info["columns"] or schema.get(table)
        if not columns:
            logging.warning("Skipping table %s; column names unknown", table)
            continue
        rows = info["rows"]
        total = math.ceil(len(rows) / chunk) or 1
        for part in range(total):
            part_rows = rows[part * chunk : (part + 1) * chunk]
            suffix = f"Part{part + 1}" if total > 1 else ""
            class_name = f"{camel_case(table)}Seeder{suffix}"
            file_path = output_dir / f"{class_name}.php"
            with file_path.open("w", encoding="utf-8") as fh:
                fh.write("<?php\n\n")
                fh.write("namespace Database\\Seeders;\n\n")
                fh.write("use Illuminate\\Database\\Seeder;\n")
                fh.write("use Illuminate\\Support\\Facades\\DB;\n\n")
                fh.write(f"class {class_name} extends Seeder\n{{\n")
                fh.write("    public function run(): void\n    {\n")
                fh.write(f"        DB::table('{table}')->insert([\n")
                for row in part_rows:
                    values = ", ".join(f"'{col}' => {php_value(val)}" for col, val in zip(columns, row))
                    fh.write(f"            [{values}],\n")
                fh.write("        ]);\n    }\n}\n")
            logging.info("Wrote %s", file_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert SQL dumps to Laravel seeders")
    parser.add_argument("sql", help="SQL file or directory containing .sql files")
    parser.add_argument("--schema", help="SQL file describing tables (CREATE TABLE)")
    parser.add_argument("--output", default="seeders_out", help="Directory for generated seeders")
    parser.add_argument("--chunk", type=int, default=1000, help="Max rows per seeder class")
    args = parser.parse_args()

    input_path = Path(args.sql)
    sql_files = [input_path] if input_path.is_file() else list(input_path.glob("*.sql"))

    schema: Dict[str, List[str]] = {}
    if args.schema:
        schema_text = Path(args.schema).read_text(encoding="utf-8", errors="ignore")
        schema = parse_schema(schema_text)

    aggregated: Dict[str, Dict[str, List]] = {}
    for path in sql_files:
        logging.info("Parsing %s", path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        inserts = parse_inserts(text)
        for table, info in inserts.items():
            entry = aggregated.setdefault(table, {"columns": info["columns"], "rows": []})
            if not entry["columns"]:
                entry["columns"] = info["columns"]
            entry["rows"].extend(info["rows"])
    generate_seeders(aggregated, schema, Path(args.output), args.chunk)


if __name__ == "__main__":
    main()
