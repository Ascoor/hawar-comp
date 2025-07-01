#!/usr/bin/env python
"""Utility to load legacy SQL files into a MySQL database."""
import argparse
import logging
from pathlib import Path
from sqlalchemy import create_engine

from transform_legacy_db import process_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run(db_conn: str, input_dir: Path) -> None:
    """Process all `.sql` files from *input_dir* and load them using *db_conn*."""
    engine = create_engine(db_conn)
    for sql_file in input_dir.glob("*.sql"):
        try:
            process_file(sql_file, engine)
        except Exception as exc:
            logging.exception("Failed to process %s: %s", sql_file, exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load legacy SQL files into MySQL")
    parser.add_argument(
        "--db",
        default="mysql+pymysql://askar:Askar@1984@127.0.0.1:3306/askar",
        help="SQLAlchemy connection string",
    )
    parser.add_argument(
        "--dir",
        default="sqls",
        help="Directory containing legacy SQL files",
    )
    args = parser.parse_args()
    run(args.db, Path(args.dir))


if __name__ == "__main__":
    main()
