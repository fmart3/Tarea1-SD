import requests

def add_car(*args):
    url = "http://localhost:5000/api/cars"
    id, brand, model, color, registration_date, year, price_in_euro, power_kw, power_ps, transmission_type, fuel_type, fuel_consumption_l_100km, fuel_consumption_g_km, mileage_in_km, offer_description = args
    
    payload = {
        'id': id,
        'brand': brand,
        'model': model,
        'color': color,
        'registration_date': registration_date,
        'year': year,
        'price_in_euro': price_in_euro,
        'power_kw': power_kw,
        'power_ps': power_ps,
        'transmission_type': transmission_type,
        'fuel_type': fuel_type,
        'fuel_consumption_l_100km': fuel_consumption_l_100km,
        'fuel_consumption_g_km': fuel_consumption_g_km,
        'mileage_in_km': mileage_in_km,
        'offer_description': offer_description
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Car added successfully")
    else:
        print("Failed to add car:", response.status_code, response.text)


def get_cars_by_brand(brand):
    url = f"http://localhost:5000/api/cars/brand"
    params = {'brand': brand}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve cars by brand:", response.status_code)
        return None

def get_books():
    url = "http://localhost:5000/api/books"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve books:", response.status_code)
        return None
    
def get_book_by_title(title):
    url = f"http://localhost:5000/api/books"
    params = {'title': title}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve book by title:", response.status_code)
        return None
    
def get_books_by_year(year):
    url = "http://localhost:5000/api/books"
    params = {'original_publication_year': year}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve books from 2008:", response.status_code)
        return None

def run():
    # Add a new car
    add_car(50074,'toyota','Toyota Corolla','blue','05/2020',2020,21500,88,107,'Automatic','Petrol',"6 l/100 km","125 g/km",55.0,'Corolla Hybrid Excel')

    # Retrieve cars with brand = "Ford"
    ford_cars = get_cars_by_brand("ford")
    if ford_cars:
        print("Cars with brand 'Ford':", ford_cars)
    else:
        print("No cars found with brand 'Ford'")

    #Retrieve book Divergent
    title = "Divergent (Divergent, #1)"
    book = get_book_by_title(title)
    if book:
        print("Book retrieved by title:", book)
    else:
        print("Book not found with title", title)
    
if __name__ == '__main__':
    run()
