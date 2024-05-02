import requests
from urllib.parse import urljoin
from datetime import datetime
from config import API_URL

def parsing(products_count):
    base_url = API_URL
    endpoint = '/api/products/'
    url = urljoin(base_url, endpoint)
    headers = {'Content-Type': 'application/json'}
    if products_count:
        data = {'products_count': products_count}
    else:
        data = {}

    response = None

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        if response.status_code == 201:
            response = str(response.json())
            return response, None
        else:
            return None, response
        
    except requests.RequestException as e:
        print(f"Произошла ошибка: {e}")


def get_products_list():
    base_url = API_URL
    endpoint = '/api/products/'
    url = urljoin(base_url, endpoint)
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            response = response.json()
            return response
        
    except requests.RequestException as e:
        print(f"Произошла ошибка: {e}")

def get_product(product_id):
    base_url = API_URL
    endpoint = f'/api/products/{product_id}'
    url = urljoin(base_url, endpoint)
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            response = response.json()
            return response
        
    except requests.RequestException as e:
        print(f"Произошла ошибка: {e}")
   