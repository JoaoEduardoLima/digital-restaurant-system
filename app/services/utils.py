MAX_AGE_COOKIE = 60*60*3 # 3 hours

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def translate_status_customer(status):
    """Translate order status to Customer"""
    # 'pending', 'in_progress', 'ready'
    translations = {
        "pending": "Sent to Kitchen",
        "in_progress": "We are preparing your order",
        "ready": "Ready!",
    }
    return translations.get(status, status)

def translate_status_restaurant(status):
    """Translate order status to Kitchen"""
    # 'pending', 'in_progress', 'ready'
    translations = {
        "pending": "Pending",
        "in_progress": "In Progress",
        "ready": "Ready",
    }
    return translations.get(status, status)

# [{'customer_name': 'João', 'order_status': 'pending', 'item_name': 'bacon burger', 'amount': 1, 'note': ''},
#  {'customer_name': 'João', 'order_status': 'pending', 'item_name': 'bacon burger', 'amount': 2, 'note': ''}, 
#  {'customer_name': 'João', 'order_status': 'pending', 'item_name': 'bacon burger', 'amount': 1, 'note': ''},
#  {'customer_name': 'João', 'order_status': 'pending', 'item_name': 'fries', 'amount': 1, 'note': ''}]
def group_items_by_customer(items):
    """Group items by customer name"""
    grouped_items = []
    for item in items:
        # Check if the customer already exists in the grouped_items
        existing_customer = next((customer for customer in grouped_items if customer["customer_name"] == item["customer_name"]), None)
        if existing_customer:
            # If the customer exists, append the item to their list
            existing_customer["items"].append({
                "item_name": item["item_name"],
                "amount": item["amount"],
                "note": item["note"],
                "order_status": item["order_status"],
                "order_updated_at": item["order_updated_at"]
            })
        else:
            # If the customer doesn't exist, create a new entry
            grouped_items.append({
                "customer_name": item["customer_name"],
                "items": [{
                    "item_name": item["item_name"],
                    "amount": item["amount"],
                    "note": item["note"],
                    "order_status": item["order_status"],
                    "order_updated_at": item["order_updated_at"]
                }]
            })
    return grouped_items

def group_orders_by_id(orders):
    """Group orders by order_id"""
    grouped_orders = []
    for order in orders:
        order_id = order["order_id"]
        existing_order = next((o for o in grouped_orders if o["order_id"] == order_id), None)
        if existing_order:
            existing_order["items"].append({
                "item_name": order["item_name"],
                "amount": order["amount"],
                "note": order["note"]
            })
        else:
            grouped_orders.append({
                "order_id": order_id,
                "customer_name": order["customer_name"],
                "table_number": order["table_number"],
                "order_status": order["order_status"],
                "order_updated_at": order["order_updated_at"],
                "items": [{
                    "item_name": order["item_name"],
                    "amount": order["amount"],
                    "note": order["note"]
                }]
            })
    return grouped_orders