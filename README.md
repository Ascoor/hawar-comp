# Hawar Club Management

This repository contains the React frontend and database schema for the Hawar Club management system. The backend source code is not included but the application expects it to expose a REST API.

## Initializing the Database

1. Create a new database in your SQL server.
2. Load the SQL dumps from `backend/sqls` into the database. For example with MySQL:
   ```bash
   mysql -u <user> -p <database_name> < backend/sqls/members.sql
   ```
   If you are using SQL Server, execute `VW_MEMBERSFEES.sql` with `sqlcmd` or your preferred tool.

## Starting the Backend

Run your backend service so that it listens on `http://localhost:8000` (or any URL you prefer). The frontend reads this value from `frontend/src/config.js`.

## Running the Frontend

See [frontend/README.md](frontend/README.md) for details on installing dependencies and running the React development server.
