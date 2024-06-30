import json
from collections import OrderedDict
from flask import Flask, Response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import psycopg2
from psycopg2 import pool
from urllib.parse import unquote_plus

app = Flask(__name__)

# Load config file
with open('config.json', 'r') as config:
    config = json.load(config)

db_params = config['db_params']
db_table = config['db_table']

# Create connection pool
try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(1, 5, **db_params)
    print("Connection pool created successfully.")
except (Exception, psycopg2.Error) as error:
    print("Error creating PostgreSQL connection pool:", error)

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{config['rate_limit']} per minute"]
)
limiter.init_app(app)  # Initialize the limiter with the Flask app

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/item/<name>', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Cache response for 60 seconds
def get_strain_by_name(name):
    try:
        decoded_name = unquote_plus(name) # Decode name to remove spaces
        conn = conn_pool.getconn() # Connect to db pool

        query = f"SELECT * FROM {db_table} WHERE name ILIKE %s;"
        
        with conn.cursor() as cur:
            
            # Execute SQL query with (% wildcard for ILIKE) parameter searching without case-sensitivity
            cur.execute(query, ('%' + decoded_name + '%',))
            # Get column names from the cursors description
            columns = [desc[0] for desc in cur.description]
            # Fetch all rows from the executed query and create a list of dictionaries
            result = [dict(zip(columns, row)) for row in cur.fetchall()]

        conn_pool.putconn(conn)

        if result:
            # Sort the json
            json_result = json.dumps(result)
            # Return JSON response as json content type
            return Response(json_result, content_type='application/json')
        else:
            return jsonify({'message': 'Strain not found'}), 404
    
    except (Exception, psycopg2.Error) as error:
        print("Error pulling data:", error)
        return jsonify({'error': 'Failed to pull data.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
