import sqlite3

class Store:
    def __init__(self, db_name='shoeStore.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('DELETE FROM shoes')
        self.conn.commit()

        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="shoes"')
        self.conn.commit()

        self.cursor.executemany('INSERT INTO shoes (brand, model, price) VALUES (?, ?, ?)', [
            ('Nike', 'Air Max', 149.0),
            ('Adidas', 'Superstar', 99.0),
            ('Puma', 'Suede Classic', 79.0),
            ('Reebok', 'Club C 85', 89.0),
            ('Vans', 'Old Skool', 69.0),
            ('Converse', 'Chuck Taylor All Star', 59.0)
        ])
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS basket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                shoe_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(shoe_id) REFERENCES shoes(id)
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                address TEXT,
                amount REAL,
                order_number INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
