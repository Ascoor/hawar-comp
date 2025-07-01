# hawar-comp

## Database schema

The repository contains SQL dumps under `backend/sqls`. In addition to the data exports a script named `create_tables.sql` provides the table definitions. The main relationships are:

- `Fees.Fee_Mem_ID` references `Members.Mem_ID`.

Run the `create_tables.sql` script before importing any dump so that the required tables exist with the correct foreign keys.
