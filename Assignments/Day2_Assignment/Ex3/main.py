import requests
import json
import os

file_path = r"D:\Sunbeam\SUNBEAM_ASSIGNMENTS-IIT-GEN-AI-94574\Assignments\Day2_Assignment\Ex3\data.json"
base_url = "https://dummyjson.com/carts"

def get_cart_by_id(cart_id):
    url = f"{base_url}/{cart_id}"
    response = requests.get(url)

    if response.status_code == 200:
        cart = response.json()

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(file_path, "w") as f:
            json.dump(cart, f, indent=4)

        print(f"Cart saved successfully to:\n{file_path}")
        return cart
    else:
        print("Failed to retrieve data")
        return None

cart_id = input("Enter cart id: ")
get_cart_by_id(cart_id)
