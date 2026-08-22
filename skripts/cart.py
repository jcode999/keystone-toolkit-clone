import requests
from pathlib import Path
import json
from dataclasses import dataclass

def get_store():
    PROJECT_DIR = Path(__file__).resolve().parent.parent
    PACKAGE_JSON = PROJECT_DIR / "package.json"

    with open(PACKAGE_JSON) as f:
        package = json.load(f)

    store = package["config"]["store"]

    if not store.startswith("http"):
        store = f"https://{store}"

    store = store.rstrip("/")
    return store

@dataclass
class CartItem:
    id:int
    quantity:str

class Cart:
    def __init__(self,store):
        self.store = store
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def add_items(self,items:list[CartItem]):
        self.session.get(f"{self.store}/cart.js")
        response = self.session.post(
            f"{self.store}/cart/add.js",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "items": [
                    {
                        "id": item.id,
                        "quantity": item.quantity,
                    } for item in items
                ]
            },
        )

        print("adding to cart [status]: ", response.status_code)
        print("response text: \n", response.text)
        return response.json()


cart = Cart(store=get_store())
cart_items = [
    CartItem(id=52070264963361, quantity=1),
    CartItem(id=52070264996129, quantity=101),

]
cart.add_items(cart_items)