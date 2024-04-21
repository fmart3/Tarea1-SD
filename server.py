import grpc
import cache_pb2
import cache_pb2_grpc
from flask import Flask, jsonify, request, g
import psycopg2
import redis
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_grpc_client():
    channel = grpc.insecure_channel('localhost:50051')
    return cache_pb2_grpc.CacheStub(channel)


# Connect to PostgreSQL
def get_db():
    if 'db' not in g:
        try:
            g.db = psycopg2.connect(
                dbname="sd",
                user="postgres",
                password="hola1102",
                host="localhost",
                port="5432"
            )
        except psycopg2.Error as e:
            logging.error("Failed to connect to PostgreSQL: %s", e)
            raise
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize Redis
def get_redis_client():
    if 'redis_client' not in g:
        try:
            g.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        except redis.RedisError as e:
            logging.error("Failed to connect to Redis: %s", e)
            raise
    return g.redis_client

# Routes for Cache
@app.route('/api/cache/get', methods=['GET'])
def get_cache():
    key = request.args.get('key')
    client = get_grpc_client()
    try:
        response = client.Get(cache_pb2.GetRequest(key=key))
        return jsonify({'value': response.value})
    except grpc.RpcError as e:
        logging.error("gRPC error while getting cache: %s", e)
        return jsonify({'error': 'Failed to retrieve value from cache'}), 500

@app.route('/api/cache/set', methods=['POST'])
def set_cache():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    client = get_grpc_client()
    try:
        response = client.Set(cache_pb2.SetRequest(key=key, value=value))
        return jsonify({'message': 'Value set in cache'})
    except grpc.RpcError as e:
        logging.error("gRPC error while setting cache: %s", e)
        return jsonify({'error': 'Failed to set value in cache'}), 500

# Routes for Cars and Books
@app.route('/api/cars', methods=['GET'])
def get_cars():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM cars;")
        cars = cur.fetchall()
        return jsonify(cars)
    except psycopg2.Error as e:
        logging.error("PostgreSQL error while fetching cars: %s", e)
        return jsonify({'error': 'Failed to fetch cars from database'}), 500
    finally:
        cur.close()

@app.route('/api/books', methods=['GET'])
def get_books():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        return jsonify(books)
    except psycopg2.Error as e:
        logging.error("PostgreSQL error while fetching books: %s", e)
        return jsonify({'error': 'Failed to fetch books from database'}), 500
    finally:
        cur.close()

if __name__ == '__main__':
    app.run(debug=True)
