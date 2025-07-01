 
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
 
# hawar-comp

 
## Database schema

The repository contains SQL dumps under `backend/sqls`. In addition to the data exports a script named `create_tables.sql` provides the table definitions. The main relationships are:

- `Fees.Fee_Mem_ID` references `Members.Mem_ID`.

Run the `create_tables.sql` script before importing any dump so that the required tables exist with the correct foreign keys.

## Configuration

The React frontend reads its API endpoint from `frontend/src/config.js`. The file exports an object with a `baseURL` property pointing to the backend server:

```javascript
const API_CONFIG = {
  baseURL: 'http://localhost:8000',
};

export default API_CONFIG;
```

Modify `baseURL` to match the host and port of your API. For example, when running in production you might set it to `https://api.example.com`. You can create different copies of this file for development, staging, and production environments as needed.

## Seeding Example Data

Run the Laravel seeders after configuring your `.env` connection:

```bash
php artisan migrate
php artisan db:seed
```

This populates the lookup tables (`member_category`, `member_relation`, `member_status`, `membership_renew_settings`) and a few sample records in `member_details`.


## Data Migration

For instructions on migrating legacy membership records into the Laravel schema see [docs/migration.md](docs/migration.md).
