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
            return None
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_redis_client():
    if 'redis_client' not in g:
        try:
            g.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        except redis.RedisError as e:
            logging.error("Failed to connect to Redis: %s", e)
            return None
    return g.redis_client

@app.route('/api/cache/get', methods=['GET'])
def get_cache():
    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'Key parameter is missing'}), 400

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
    if not key or not value:
        return jsonify({'error': 'Key or value parameter is missing'}), 400

    client = get_grpc_client()
    try:
        response = client.Set(cache_pb2.SetRequest(key=key, value=value))
        return jsonify({'message': 'Value set in cache'})
    except grpc.RpcError as e:
        logging.error("gRPC error while setting cache: %s", e)
        return jsonify({'error': 'Failed to set value in cache'}), 500
    
@app.route('/api/cars', methods=['POST'])
def add_car():
    data = request.json
    id = data.get('id')
    brand = data.get('brand')
    model = data.get('model')
    color = data.get('color')
    registration_date = data.get('registration_date')
    year = data.get('year')
    price_in_euro = data.get('price_in_euro')
    power_kw = data.get('power_kw')
    power_ps = data.get('power_ps')
    transmission_type = data.get('transmission_type')
    fuel_type = data.get('fuel_type')
    fuel_consumption_l_100km = data.get('fuel_consumption_l_100km')
    fuel_consumption_g_km = data.get('fuel_consumption_g_km')
    mileage_in_km = data.get('mileage_in_km')
    offer_description = data.get('offer_description')

    return jsonify({'message': 'Car added successfully'}), 200

@app.route('/api/cars', methods=['GET'])
def get_cars():
    db = get_db()
    if not db:
        return jsonify({'error': 'Failed to connect to PostgreSQL'}), 500

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

@app.route('/api/cars/brand', methods=['GET'])
def get_cars_by_brand():
    brand = request.args.get('brand')
    if not brand:
        return jsonify({'error': 'Brand parameter is missing'}), 400

    db = get_db()
    if not db:
        return jsonify({'error': 'Failed to connect to PostgreSQL'}), 500

    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM cars WHERE brand = %s LIMIT 10;", (brand,))
        cars = cur.fetchall()
        return jsonify(cars)
    except psycopg2.Error as e:
        logging.error("PostgreSQL error while fetching cars by brand: %s", e)
        return jsonify({'error': 'Failed to fetch cars by brand from database'}), 500
    finally:
        cur.close()

@app.route('/api/books', methods=['GET'])
def get_books():
    db = get_db()
    if not db:
        return jsonify({'error': 'Failed to connect to PostgreSQL'}), 500

    title = request.args.get('title')
    if title:
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM books WHERE title = %s;", (title,))
            books = cur.fetchall()
            return jsonify(books)
        except psycopg2.Error as e:
            logging.error("PostgreSQL error while fetching books by title: %s", e)
            return jsonify({'error': 'Failed to fetch books by title from database'}), 500
        finally:
            cur.close()
    else:
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
