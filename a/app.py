from flask import Flask, jsonify, request, g
import grpc
import cache_pb2
import cache_pb2_grpc
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname="sd",
            user="postgres",
            password="hola1102",
            host="localhost",
            port="5432"
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# gRPC client initialization
def get_grpc_client():
    if 'grpc_client' not in g:
        channel = grpc.insecure_channel('localhost:50051')
        g.grpc_client = cache_pb2_grpc.CacheStub(channel)
    return g.grpc_client

# Routes
@app.route('/cache/get', methods=['GET'])
def get_cache():
    key = request.args.get('key')
    client = get_grpc_client()
    response = client.Get(cache_pb2.GetRequest(key=key))
    return jsonify({'value': response.value})

@app.route('/cache/set', methods=['POST'])
def set_cache():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    client = get_grpc_client()
    response = client.Set(cache_pb2.SetRequest(key=key, value=value))
    return jsonify({'message': 'Value set in cache'})

@app.route('/cars', methods=['GET'])
def get_cars():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM cars;")
    cars = cur.fetchall()
    cur.close()
    return jsonify(cars)

@app.route('/books', methods=['GET'])
def get_books():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM books;")
    books = cur.fetchall()
    cur.close()
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)