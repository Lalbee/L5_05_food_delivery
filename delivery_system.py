"""Food delivery order queue manager."""
import itertools
import json
from datetime import datetime

# Shared state (modified in place, so no 'global' statements are needed)
orders = {}
menu = {}
ID_COUNTER = itertools.count(1)
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]


def create_order(customer, items, order_history=None):
    """Create an order, store it, and return its id."""
    if order_history is None:
        order_history = []
    total = 0
    for i in items:
        total += menu.get(i, 99)  # unknown dishes silently cost 99
    order_id = next(ID_COUNTER)
    orders[order_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed",
    }
    order_history.append(order_id)
    return order_history[-1]


def update_order_status(order_id, status):
    """Change an order's status. Return True on success, False otherwise."""
    if status not in VALID_STATUSES:
        print(f"Invalid status: {status}")
        return False
    try:
        orders[order_id]["status"] = status
        return True
    except KeyError:
        print(f"Order {order_id} not found")
        return False


def read_menu_config(file="menu.json"):
    """Load the menu from a JSON file, or use a default menu."""
    menu.clear()
    try:
        with open(file, encoding="utf-8") as f:
            menu.update(json.load(f))
    except (OSError, json.JSONDecodeError):
        menu.update({"pizza": 250, "burger": 150, "fries": 90, "coke": 40})


def daily_revenue():
    """Return the total of all delivered orders."""
    revenue = 0
    for order in orders.values():
        if order["status"] == "delivered":
            revenue = revenue + order["total"]
    return revenue


def backup_orders(file="orders.json"):
    """Save all orders to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(orders, f)


def restore_orders(file="orders.json"):
    """Load orders back from a JSON file."""
    with open(file, encoding="utf-8") as f:
        loaded = {int(k): v for k, v in json.load(f).items()}
    orders.clear()
    orders.update(loaded)


def print_queue():
    """Print every order in the queue."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(order_id, order["customer"], order["status"], order["total"])


def main():
    """Run a demo of the order queue."""
    read_menu_config()
    a = create_order("Asha", ["pizza", "coke"])
    b = create_order("Ravi", ["burger", "sushi"])
    c = create_order("", [])
    update_order_status(a, "delivered")
    update_order_status(b, "teleported")
    update_order_status(42, "delivered")
    update_order_status(c, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()