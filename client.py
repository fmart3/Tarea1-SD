import requests

def add_car(make, model):
    url = "http://localhost:5000/api/cars"
    payload = {'make': make, 'model': model}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Car added successfully")
    else:
        print("Failed to add car:", response.status_code, response.text)

def get_books():
    url = "http://localhost:5000/api/books"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve books:", response.status_code)
        return None

def run():
    # Add a new car
    add_car("Toyota", "Camry")

    # Retrieve all cars
    books = get_books()
    if books:
        print("Books retrieved from database:", books)
    else:
        print("No books found in database")

if __name__ == '__main__':
    run()
