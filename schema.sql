CREATE TABLE
    user (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );

-- username: admin
-- password: admin123
INSERT INTO
    user (username, password)
VALUES
    (
        'admin',
        'scrypt:32768:8:1$bMtld7aARgyBLRvx$8fbc2bd69ea54689adc747eb2b9c0f70d6633ed27677c471790d2d043d24f8cd07e8d04fdc1f7415df4be144acc8373dcf4fa644af3ebacfe5227c34ae5017c1'
    );

CREATE TABLE
    customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        table_number INTEGER NOT NULL,
        name TEXT NOT NULL
    );

CREATE TABLE
    orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_customer INTEGER NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('pending', 'in_progress', 'ready')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_customer) REFERENCES customer (id)
    );

CREATE TABLE
    item (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        price NUMERIC NOT NULL,
        category TEXT NOT NULL CHECK (category IN ('food', 'dessert', 'drinks')),
        available BOOLEAN NOT NULL,
        image_url TEXT
    );

CREATE TABLE
    item_by_order (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_order INTEGER NOT NULL,
        id_item INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        note TEXT,
        status TEXT NOT NULL CHECK (status IN ('payed', 'canceled', 'pending'))
        FOREIGN KEY (id_order) REFERENCES orders (id),
        FOREIGN KEY (id_item) REFERENCES item (id)
    );

CREATE TRIGGER update_order_timestamp AFTER
UPDATE OF status ON orders FOR EACH ROW BEGIN
UPDATE orders
SET
    updated_at = CURRENT_TIMESTAMP
WHERE
    id = NEW.id;

END;

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'bacon burger',
        7.50,
        'food',
        1,
        '/static/images/bacon-burger.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'cheeseburger',
        7.00,
        'food',
        1,
        '/static/images/cheeseburger.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'kids burger',
        5.50,
        'food',
        1,
        '/static/images/kids-burger.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'vegan burger',
        8.50,
        'food',
        1,
        '/static/images/vegan-burger.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'fries',
        2.50,
        'food',
        1,
        '/static/images/fries.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'salad',
        2.50,
        'food',
        1,
        '/static/images/salad.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'cola',
        3.00,
        'drinks',
        1,
        '/static/images/cola.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'orange juice',
        3.00,
        'drinks',
        1,
        '/static/images/orange-juice.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'water',
        2.00,
        'drinks',
        1,
        '/static/images/water.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'lemon tea',
        2.50,
        'drinks',
        1,
        '/static/images/lemon-tea.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'pancake',
        7.00,
        'dessert',
        1,
        '/static/images/pancake.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'waffle',
        7.00,
        'dessert',
        1,
        '/static/images/waffle.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'pudding',
        8.50,
        'dessert',
        1,
        '/static/images/pudding.png'
    );

INSERT INTO
    item (name, price, category, available, image_url)
VALUES
    (
        'vanilla ice cream',
        3.00,
        'dessert',
        1,
        '/static/images/vanilla-ice-cream.png'
    );