# Legacy DB Transformer

This utility cleans and restructures SQL dump files from older systems. It can produce new SQL files or load the data into a staging database for further processing.

## Installation

Install the required packages with:

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env` and adjust values:
   - `INPUT_DIR` - folder containing legacy `.sql` files
   - `OUTPUT_DIR` - folder to write cleaned inserts
   - `DB_CONN_STRING` - SQLAlchemy connection string for an optional staging DB

## Usage

Run the transformation script:

```bash
python transform_legacy_db.py
```

The script reads all `*.sql` files from `INPUT_DIR`, fixes the relationships, and writes new insert statements to `OUTPUT_DIR` or inserts them directly into the configured database.

## Input/Output Format

* **Input**: SQL dump files containing `INSERT` statements.
* **Output**: Cleaned `INSERT` files in the output directory or data inserted into a staging database.

Progress and errors are logged to stdout using Python's `logging` module.

### Example MySQL Transfer

For a quick start with MySQL you can use the helper script `transfer_sqls.py`.
It reads all `.sql` files from the `sqls` folder and loads them into the
database specified by the connection string:

```bash
python transfer_sqls.py \
  --db mysql+pymysql://askar:Askar@1984@127.0.0.1:3306/askar
```

Make sure `pymysql` is installed by installing `requirements.txt` first.
