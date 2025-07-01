import logging
import os
from pathlib import Path
from typing import List


import pandas as pd
import sqlparse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    input_dir = Path(os.getenv("INPUT_DIR", "legacy_dumps"))
    output_dir = Path(os.getenv("OUTPUT_DIR", "clean_dumps"))
    db_conn = os.getenv("DB_CONN_STRING")
    output_dir.mkdir(parents=True, exist_ok=True)
    return input_dir, output_dir, db_conn


def parse_inserts(sql_text: str) -> List[pd.DataFrame]:
    """Parse INSERT statements and return a list of DataFrames."""
    inserts = []
    for statement in sqlparse.split(sql_text):
        stmt = sqlparse.parse(statement)[0]
        if stmt.get_type() != "INSERT":
            continue
        tokens = [t for t in stmt.tokens if not t.is_whitespace]
        try:
            table = tokens[2].get_name()
            columns = [c.get_name() for c in tokens[3].get_parameters()]  # type: ignore
            values_token = tokens[-1]
            rows = []
            for group in values_token.get_sublists():
                vals = [v.value.strip("'\"") for v in group.get_sublists()]
                rows.append(vals)
            df = pd.DataFrame(rows, columns=columns)
            df["__table"] = table
            inserts.append(df)
        except Exception as exc:
            logging.error("Malformed INSERT statement skipped: %s", exc)
    return inserts


def fix_relationships(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder for relationship cleanup logic."""
    # Example: fill missing parent_id with 0
    if "parent_id" in df.columns:
        df["parent_id"] = df["parent_id"].fillna(0)
    return df


def process_file(path: Path, engine=None):
    logging.info("Processing %s", path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    frames = parse_inserts(text)
    for df in frames:
        df = fix_relationships(df)
        table = df.pop("__table").iloc[0]
        if engine:
            logging.info("Inserting %d rows into %s", len(df), table)
            df.to_sql(table, engine, if_exists="append", index=False)
        else:
            output_path = Path("clean_dumps") / f"{table}.sql"
            with output_path.open("a", encoding="utf-8") as fh:
                for _, row in df.iterrows():
                    cols = ", ".join(df.columns)
                    vals = ", ".join(f"'{str(v)}'" for v in row)
                    fh.write(f"INSERT INTO {table} ({cols}) VALUES ({vals});\n")


def main():
    input_dir, _, db_conn = load_config()
    engine = create_engine(db_conn) if db_conn else None
    for sql_file in input_dir.glob("*.sql"):
        try:
            process_file(sql_file, engine)
        except Exception as exc:
            logging.exception("Failed to process %s: %s", sql_file, exc)


if __name__ == "__main__":
    main()
