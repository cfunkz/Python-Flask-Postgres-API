# Python-Flask-Postgres-API
A simple API example using python, flask and postgres sql with pooling, caching and rate limit for requests.

## Requirements
- `pip install flask`
- `pip install psycopg2`
- `pip install Flask-Limiter`
- `pip install Flask-Caching`

## How to use
- Edit the `config.json` file adding your database details from which you want to pull the data
- Run the `main.py` file
- Visit `http://localhost:5000/item/<name>` to search for items with that name

![image](https://github.com/cfunkz/Python-Flask-Postgres-API/assets/116670695/e92fb655-5128-4c51-b6ff-a5703fea30a5)
