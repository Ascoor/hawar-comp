# Hawar Frontend

This folder contains the React application for the Hawar Club management system.

## Prerequisites

- [Node.js](https://nodejs.org/) and npm installed on your machine.

## Installing Dependencies

```bash
cd frontend
npm install
```

## Configuration

The frontend expects a configuration file at `src/config.js` containing the base URL for the backend API. Create the file with the following contents and adjust the URL if your backend runs elsewhere:

```javascript
// src/config.js
const API_CONFIG = {
  baseURL: 'http://localhost:8000'
};
export default API_CONFIG;
```

Alternatively you can provide the value via environment variables and import it in your code.

## Initializing the Database

Before starting the services make sure you have created a database and imported the SQL dumps located in `../backend/sqls`. See the repository root `README.md` for details.

## Running the Services

1. Start your backend service (for example a Laravel API using `php artisan serve`) so that it matches the `baseURL` configured above.
2. Start the React development server:
   ```bash
   npm start
   ```
   The application will be available at [http://localhost:3000](http://localhost:3000).
