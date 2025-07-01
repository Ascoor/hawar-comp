# Hawar Laravel Backend

This directory contains a minimal Laravel setup intended to expose API endpoints used by the React frontend.

## Setup

1. Ensure PHP 8.1+ and Composer are installed.
2. Run `composer install` inside this directory to pull in Laravel and its dependencies.
3. Copy `.env.example` to `.env` and update the database credentials.
4. Run `php artisan key:generate` to generate the application key.
5. Run migrations to create the necessary tables.

```
php artisan migrate
```

Start the development server with:

```
php artisan serve
```

## API Endpoints

- `POST /api/register` – Register a new user.
- `POST /api/login` – Obtain an auth token.
- `POST /api/logout` – Revoke the current auth token.
- `GET /api/member-count` – Get member statistics.
- `GET /api/members/search?searchTerm=` – Search members by name or code.

These endpoints correspond to requests made by the React application.
