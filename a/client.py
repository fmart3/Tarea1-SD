import requests

def set_cache(key, value):
    url = "http://localhost:5000/cache/set"
    payload = {'key': key, 'value': value}
    response = requests.post(url, json=payload)
    return response.json()

def get_cache(key):
    url = f"http://localhost:5000/cache/get?key={key}"
    response = requests.get(url)
    return response.json()

def run():
    # Set a value in the cache
    set_cache("my_key", "my_value")

    # Retrieve the value from the cache
    response = get_cache("my_key")
    print("Value retrieved from cache:", response['value'])

if __name__ == '__main__':
    run()
