import requests

def set_cache(key, value):
    url = "http://127.0.0.1:5000/api/cache/set"
    payload = {'key': key, 'value': value}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Cache set successfully")
    else:
        print("Failed to set cache:", response.status_code, response.text)

def get_cache(key):
    url = f"http://127.0.0.1:5000/api/cache/get?key={key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve value from cache:", response.status_code)
        return None

def run():
    # Set a value in the cache
    set_cache("my_key", "my_value")

    # Retrieve the value from the cache
    response = get_cache("my_key")
    if response:
        print("Value retrieved from cache:", response['value'])
    else:
        print("Value not found in cache")

if __name__ == '__main__':
    run()
