import os
import time
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = "https://api.mercadolibre.com"
def make_request(
    method: str,
    endpoint: str,
    access_token: str,
    params: dict = None,
    data: dict = None,
    json: dict = None,
):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request(
            method, url, params=params, data=data, json=json, headers=headers
        )
        time.sleep(0.5)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)
        return None


def get_full_operations(access_token, seller_id, inventory_id, date_from, date_to):
    print(
        "GET Meli Full Operations access_token: {} | inventory_id : {} | date_from: {} | date_to: {}".format(
            access_token, inventory_id, date_from, date_to
        )
    )
    url = "/stock/fulfillment/operations/search?seller_id={}&inventory_id={}&date_from={}&date_to={}".format(
        seller_id, inventory_id, date_from, date_to
    )
    return make_request("get", url, access_token)


def get_full_stock(access_token, inventory_id):
    print(
        "GET Meli Full stock access_token: {} | inventory_id: {}".format(
            access_token, inventory_id
        )
    )
    url = "/inventories/{}/stock/fulfillment".format(inventory_id)
    return make_request("get", url, access_token)


def get_listings(access_token, seller_id, offset=0):
    print("GET Meli Listings token: {} ".format(access_token))
    url = "/users/{}/items/search?offset={}&logistic_type=fulfillment".format(seller_id, offset)
    return make_request("get", url, access_token)


def get_listings_with_ids(access_token, seller_id, item_ids):
    url = "/items?ids={}&include_attributes=all".format(",".join(item_ids))
    return make_request("get", url, access_token)

if __name__ == '__main__':
    seller_id = int(os.environ.get('SELLER_ID'))
    access_token = os.environ.get('ACCESS_TOKEN')
    
    listings_ids_data = get_listings(access_token, seller_id)
    listing_ids = listings_ids_data.get('results')
    listings_data = get_listings_with_ids(access_token, seller_id, listing_ids[:20])
    listings_data = [listing_data.get("body") for listing_data in listings_data]

    for listing_data in listings_data:
        if listing_data.get("inventory_id"):
            inventory_id = listing_data.get("inventory_id")
            full_stock_data = get_full_stock(access_token, inventory_id)
            print(full_stock_data)
            
            if full_stock_data.get("available_quantity") < 5:
                print("Stock is low")
                break
            else:
                print("Stock is ok")
            
            operations_data = get_full_operations(access_token, seller_id, inventory_id, '2025-01-01T00:00:00.000-00:00', '2025-02-07T23:59:59.000-00:00')
            print(operations_data)
            for operation in operations_data:
                if operation.get("status") == "pending":
                    print("Pending operation")
                    break
                else:
                    print("No pending operations")
            break
