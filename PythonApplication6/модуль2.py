import random
import bcrypt

class User:
    def __init__(self, store):
        self.store = store
        self.authenticated_user = None

    def validate(self, login, password):
        if not login.strip() or not password.strip():
            print("Поле логинв и пароля не могут быть пустыми. Попробуйте снова.\n")
            return False
        return True

    def authenticate(self, login, password):
        if not self.validate(login, password):
            return False

        self.store.cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        sush_user = self.store.cursor.fetchone()

        if sush_user and bcrypt.checkpw(password.encode('utf-8'), sush_user[2]):
            self.authenticated_user = sush_user
            return True
        else:
            print("Неправильный логин или пароль.\n")
            return False

    def display_products(self):
        self.store.cursor.execute('SELECT * FROM products')
        products = self.store.cursor.fetchall()
        print("Товары в магазине.\n")
        for product in products:
            print(f"{product[0]}. {product[1]} - ${product[2]}")
        return products

    def add_to_basket(self, product_id):
        self.store.cursor.execute('INSERT INTO basket (user_id, product_id) VALUES (?, ?)',
                                  (self.authenticated_user[0], product_id))
        self.store.conn.commit()

class Client(User):
    def __init__(self, store):
        super().__init__(store)

    def validate_product_id(self, product_id, products):
        try:
            product_id = int(product_id)
            if not (1 <= product_id <= len(products)):
                print(
                    "Неверный номер товара.\n")
                return False
            return True
        except ValueError:
            print(
                "Неверный ввод.\n")
            return False

    def add_to_basket(self, product_id):
        products = self.display_products()
        if not self.validate_product_id(product_id, products):
            return

        self.store.cursor.execute('INSERT INTO basket (user_id, product_id) VALUES (?, ?)',
                                  (self.authenticated_user[0], product_id))
        self.store.conn.commit()

    def display_basket(self):
        self.store.cursor.execute('''
            SELECT products.name, products.price
            FROM basket
            JOIN products ON basket.product_id = products.id
            WHERE basket.user_id = ?
        ''', (self.authenticated_user[0],))
        basket_items = self.store.cursor.fetchall()

        if basket_items:
            total_sum = sum(item[1] for item in basket_items)
            print("Товары в вашей корзине.\n")
            for item in basket_items:
                print(f"{item[0]} - ${item[1]}")
            print(f"Итого: ${total_sum}")
        else:
            print("Ваша корзина пуста.\n")

    def checkout(self):
        self.store.cursor.execute('''
            SELECT products.price
            FROM basket
            JOIN products ON basket.product_id = products.id
            WHERE basket.user_id = ?
        ''', (self.authenticated_user[0],))
        prices = self.store.cursor.fetchall()
        total_sum = sum(price[0] for price in prices)

        order_number = random.randint(1000, 9999)

        self.store.cursor.execute('''
            INSERT INTO orders (user_id, summ, order_number)
            VALUES (?, ?, ?, ?)
        ''', (self.authenticated_user[0], total_sum, order_number))
        self.store.conn.commit()

        self.store.cursor.execute('DELETE FROM basket WHERE user_id = ?', (self.authenticated_user[0],))
        self.store.conn.commit()

        print("Заказ оформлен\n")
        print(f"Ваш номер заказа №{order_number}")
        print(f"Итого: ${total_sum}")

class Administrator(User):
    admin_name = "admini"
    admin_password = "12345"

    def authenticate(self, login, password):
        return login == self.admin_name and password == self.admin_password

    def add_product(self, name, price):
        self.store.cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
        self.store.conn.commit()

    def remove_product(self, name):
        self.store.cursor.execute('DELETE FROM products WHERE name = ?', (name))
        self.store.conn.commit()

    def change_product_name(self, current_name, new_name):
        self.store.cursor.execute('UPDATE products SET name = ? WHERE name = ?', (new_name, current_name))
        self.store.conn.commit()
