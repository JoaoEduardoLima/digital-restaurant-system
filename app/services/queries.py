from app.db import get_db
import sqlite3

def get_items():
    db = get_db()
    cur = db.execute("SELECT * FROM item")
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def insert_customer(table_number, name):
    db = get_db()
    cur = db.execute("INSERT INTO customer (table_number, name) VALUES (?, ?)", (table_number, name))
    return cur.lastrowid


def insert_orders(id_customer, status):
    db = get_db()
    cur = db.execute("INSERT INTO orders (id_customer, status) VALUES (?, ?)", (id_customer, status))
    return cur.lastrowid


def insert_item_by_order(id_order, items):
    db = get_db()
    for item in items:
        db.execute("INSERT INTO item_by_order (id_order, id_item, amount, note) VALUES (?, ?, ?, ?)",
                   (id_order, item["id_item"], item["amount"], item.get("note")))


def try_new_order(table_number, name, items):
    db = get_db()
    try:
        id_customer = insert_customer(table_number, name)
        id_order = insert_orders(id_customer, "pending")
        insert_item_by_order(id_order, items)

        db.commit()
        return {"id_order": id_order, "status": "pending"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def get_item_by_order(id_order):
    db = get_db()
    cur = db.execute("""
    SELECT c.name AS customer_name,
           o.status AS order_status,
           o.updated_at AS order_updated_at,
           i.name AS item_name,
           io.amount,
           io.note
    FROM customer AS c
    JOIN orders AS o ON c.id = o.id_customer
    JOIN item_by_order AS io ON o.id = io.id_order
    JOIN item AS i ON io.id_item = i.id
    WHERE o.id = ?;
    """, (id_order,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_user_by_username(username):
    db = get_db()
    cur = db.execute("SELECT * FROM user WHERE username = ?", (username,))
    row = cur.fetchone()
    return dict(row) if row else None


# For the kitchen stream, we need open a new connection to the database each time we fetch orders,
#  because the stream runs in a separate thread and the Flask `g` object is not available there.
#  So we will create a new connection to the database each time we fetch orders for the stream.
def get_orders():
    conn = sqlite3.connect("restaurant.db")
    conn.row_factory = sqlite3.Row
    cur = conn.execute("""
        SELECT c.name AS customer_name,
               c.table_number AS table_number,
               o.id AS order_id,
               o.status AS order_status,
               o.updated_at AS order_updated_at,
               i.name AS item_name,
               io.amount,
               io.note
        FROM customer AS c
        JOIN orders AS o ON c.id = o.id_customer
        JOIN item_by_order AS io ON o.id = io.id_order
        JOIN item AS i ON io.id_item = i.id
        WHERE o.status IN ('pending', 'in_progress')
        ORDER BY o.updated_at DESC;
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_order_status(order_id, new_status):
    db = get_db()
    try:
        db.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        db.commit()
        return {"message": "Order status updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

def get_orders_by_table_checkout(table_number):
    db = get_db()
    cur = db.execute("""
        SELECT c.name AS customer_name,
               i.name AS item_name,
               io.amount,
               io.id AS item_by_order_id,
               i.price
        FROM customer AS c
        JOIN orders AS o ON c.id = o.id_customer
        JOIN item_by_order AS io ON o.id = io.id_order
        JOIN item AS i ON io.id_item = i.id
        WHERE c.table_number = ?
        AND io.status = 'pending'
    """, (table_number,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def update_item_by_order_status(item_by_order_id, new_status):
    db = get_db()
    try:
        db.execute("UPDATE item_by_order SET status = ? WHERE id = ?", (new_status, item_by_order_id))
        db.commit()
        return {"message": "Item by order status updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}