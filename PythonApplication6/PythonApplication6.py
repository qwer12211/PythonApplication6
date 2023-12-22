from класс1 import Store
from модуль1 import Client, Administrator
import bcrypt
store = Store()

while True:
    print("Чтобы войти, вам необходимо авторизоваться или зарегистрироваться\n")

    print("1 - Авторизоваться.")
    print("2 - Зарегистрироваться.")
    print("3 - Выйти.")
    choice = input("Выберите действие.\n")

    if choice == '1':
        print("Авторизация\n")
        print("1 - Авторизоваться как клиент.")
        print("2 - Авторизоваться как сотрудник.")
        print("3 - Вернуться назад.")
        choice_registration = input("Выберите действие.\n")

        if choice_registration == '1':
            client = Client(store)

            while True:
                login_clienta = input("Введите логин.\n")
                password_Clienta = input("Введите пароль.\n")

                if login_clienta.strip() and password_Clienta.strip():
                    break
                else:
                    print("Поля с логином и паролем не могут быть пустыми. Попробуйте снова.\n")

            if client.authenticate(login_clienta, password_Clienta):
                print("Авторизация выполнена.\n")
            else:
                continue

            while True:
                print("Добро пожаловать в магазин обуви 'Большевичка'\n")
                print("1 - Товары")
                print("2 - Корзина")
                print("3 - Выйти")

                client_action = input("Выберите действие.\n")

                if client_action == '1':
                    client.display_products()
                    add_to_cart = input("Введите номер товара для добавления в корзину или 'add' для возвращения назад.\n")

                    if add_to_cart == 'add':
                        continue
                    try:
                        product_id = int(add_to_cart)
                        products = client.display_products()
                        if 1 <= product_id <= len(products):
                            client.add_to_cart(product_id)
                            print(f"Товар '{products[product_id - 1][1]}' добавлен в корзину.\n")
                        else:
                            print("Неверный номер товара. Попробуйте снова.\n")
                    except ValueError:
                        print("Неверный ввод. Попробуёте снова.\n")

                elif client_action == '2':
                    client.display_cart()

                    print("1 - Оформить заказ.\n")
                    print("2 - Вернуться назад")
                    cart_choice = input("Выберите действие.\n")

                    if cart_choice == '1':
                        print("Оформление заказа\n")

                        address = input("Введите адрес доставки.\n")
                        client.checkout(address)
                        break

                    elif cart_choice == '2':
                        continue

                elif client_action == '3':
                    print("Ждём вас снова\n")
                    break

        elif choice_registration == '2':
            administrator = Administrator(store)

            while True:
                administrator_login = input("Введите логин.\n")
                administrator_password = input("Введите пароль.")

                if administrator_login.strip() and administrator_password.strip():
                    break
                else:
                    print("Поле логина и пароля не могут быть пустыми. Попробуйте снова.\n")

            if administrator.authenticate(administrator_login, administrator_password):
                print("Авторизация выполнена успешно\n")

                while True:
                    print("add - Добавить товар")
                    print("2 - Удалить товар")
                    print("3 - Изменить название товара")
                    print("4 - Выйти")

                    administrator_action = input("Выберите действие.\n")

                    if administrator_action == 'add':
                        print("Добавления товара.\n")
                        while True:
                            product_name = input("Введите название товара.\n ")
                            product_price = input("Введите цену товара.")
                            try:
                                product_price = float(product_price)
                                if product_name.strip() and product_price >= 0:
                                    administrator.add_product(product_name, product_price)
                                    print(f"Товар '{product_name}' успешно добавлен.\n")
                                    break
                                else:
                                    print("Поле название товара не может быть пустым, а поле цена не должно быть отрицательным.\n")
                            except ValueError:
                                print("Неверный формат цены. Попробуйте снова.\n")

                    elif administrator_action == '2':
                        print("Процесс удаления товара.\n")
                        while True:
                            product_name_to_delete = input("Введите название товара для удаления или 'back' для возвращения назад\n ")

                            if product_name_to_delete == 'back':
                                break

                            administrator.remove_product(product_name_to_delete)
                            print(f"Товар '{product_name_to_delete}' товар удален.\n")
                            break

                    elif administrator_action == '3':
                        print("Процесс изменения названия товара.\n")
                        while True:
                            product_name_to_change = input("Введите название товара для изменения или 'back' для возвращения назад\n")

                            if product_name_to_change == 'back':
                                break

                            new_product_name = input("Введите новое название товара: ")
                            administrator.change_product_name(product_name_to_change, new_product_name)
                            print(f"Название товара  изменено на '{new_product_name}'.\n")
                            break

                    elif administrator_action == '4':
                        print("Вы  вышли.\n")
                        break
            else:
                print("Неправильный логин или пароль. Попробуйте снова.\n")

    elif choice == '2':
        print("Регистрация\n")
        print("Логин должен быть не менее 4 символов\n")

        while True:
            login_Сlienta = input("Придумайте логин.\n")

            if len(login_Сlienta) >= 4:
                break
            else:
                print("Логин должен содержать не менее 4 символов и не должен быть пустым. Попробуйте снова.\n")

        while True:
            password_Clienta = input("Создайте пароль.")

            if len(password_Clienta) > 0:
                break
            else:
                print("Поле 'пароль' не может быть пустым.\n")

        store.cursor.execute('SELECT * FROM users WHERE login = ?', (login_Сlienta,))
        sush_user = store.cursor.fetchone()

        if sush_user:
            print("Пользователь с таким логином уже существует. Придумайте другой логин.\n")
        else:

            hashed_password = bcrypt.hashpw(password_Clienta.encode('utf-8'), bcrypt.gensalt())

            store.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login_Сlienta, hashed_password))

            store.conn.commit()

            print("Регистрация выполнена.\n")
    elif choice == '3':
        print("Вы  вышли.\n")
        break

    else:
        print("Неправильный ввод. Попробуйте снова.\n")
store.close()
