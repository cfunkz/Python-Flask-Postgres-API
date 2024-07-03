# Python-Flask-Postgres-API
A simple API example using python, flask and postgres sql with pooling, caching and rate limit for requests.

## Requirements
- `pip install flask`
- `pip install psycopg2`
- `pip install Flask-Limiter`
- `pip install Flask-Caching`

## How to use
- Edit the `config.json` file with your PostgreSQL database details
- Run the `main.py` file
- Visit `http://localhost:5000/item/<name>` to search for items with that name
