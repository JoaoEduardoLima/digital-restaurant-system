TABLE_NUMBERS = {str(i) for i in range(1, 13)} # 1 to 12

def valid_order(table_number: str , order: dict) -> dict:
    if table_number not in TABLE_NUMBERS:
        return {"error": "Invalid table"}

    name = order.get("name")
    if not name.strip():
        return {"error": "Invalid name"}
    
    items = order.get("items")
    if not items:
        return {"error": "Order must contain items"}
    
    for item in items:
        if "id_item" not in item or not isinstance(item["id_item"], int):
            return {"error": "Invalid item id"}
        if "amount" not in item or not isinstance(item["amount"], int) or item["amount"] <= 0:
            return {"error": "Invalid item amount"}
        if "note" in item and not isinstance(item["note"], str):
            return {"error": "Invalid note format"}
    return {}