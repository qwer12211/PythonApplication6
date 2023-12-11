import s
from ������1 import Store
from ������1 import Client, Administrator

store = Store()

while True:
    print("����� �����, ��� ���������� �������������� ��� ������������������\n")

    print("1 - ��������������.")
    print("2 - ������������������.")
    print("3 - �����.")
    choice = input("�������� ��������.\n")

    if choice == '1':
        print("�����������\n")
        print("1 - �������������� ��� ������.")
        print("2 - �������������� ��� ���������.")
        print("3 - ��������� �����.")
        choice_registration = input("�������� ��������.\n")

        if choice_registration == '1':
            client = Client(store)

            while True:
                login_client = input("������� �����.\n")
                password_client = input("������� ������.\n")

                if login_client.strip() and password_client.strip():
                    break
                else:
                    print("���� � ������� � ������� �� ����� ���� �������. ���������� �����.\n")

            if client.authenticate(login_client, password_client):
                print("����������� ���������.\n")
            else:
                continue

            while True:
                print("����� ���������� � ������� ����� '�����������'\n")
                print("1 - ������")
                print("2 - �������")
                print("3 - �����")

                client_action = input("�������� ��������.\n")

                if client_action == '1':
                    client.display_products()
                    add_to_cart = input("������� ����� ������ ��� ���������� � ������� ��� 'add' ��� ����������� �����.\n")

                    if add_to_cart == 'add':
                        continue
                    try:
                        product_id = int(add_to_cart)
                        products = client.display_products()
                        if 1 <= product_id <= len(products):
                            client.add_to_cart(product_id)
                            print(f"����� '{products[product_id - 1][1]}' �������� � �������.\n")
                        else:
                            print("�������� ����� ������. ���������� �����.\n")
                    except ValueError:
                        print("�������� ����. ��������� �����.\n")

                elif client_action == '2':
                    client.display_cart()

                    print("1 - �������� �����.\n")
                    print("2 - ��������� �����")
                    cart_choice = input("�������� ��������.\n")

                    if cart_choice == '1':
                        print("���������� ������\n")

                        address = input("������� ����� ��������.\n")
                        client.checkout(address)
                        break

                    elif cart_choice == '2':
                        continue

                elif client_action == '3':
                    print("��� ��� �����\n")
                    break

        elif choice_registration == '2':
            administrator = Administrator(store)

            while True:
                administrator_login = input("������� �����.\n")
                administrator_password = input("������� ������.")

                if administrator_login.strip() and administrator_password.strip():
                    break
                else:
                    print("���� ������ � ������ �� ����� ���� �������. ���������� �����.\n")

            if administrator.authenticate(administrator_login, administrator_password):
                print("����������� ��������� �������\n")

                while True:
                    print("add - �������� �����")
                    print("2 - ������� �����")
                    print("3 - �������� �������� ������")
                    print("4 - �����")

                    administrator_action = input("�������� ��������.\n")

                    if administrator_action == 'add':
                        print("���������� ������.\n")
                        while True:
                            product_name = input("������� �������� ������.\n ")
                            product_price = input("������� ���� ������.")
                            try:
                                product_price = float(product_price)
                                if product_name.strip() and product_price >= 0:
                                    administrator.add_product(product_name, product_price)
                                    print(f"����� '{product_name}' ������� ��������.\n")
                                    break
                                else:
                                    print("���� �������� ������ �� ����� ���� ������, � ���� ���� �� ������ ���� �������������.\n")
                            except ValueError:
                                print("�������� ������ ����. ���������� �����.\n")

                    elif administrator_action == '2':
                        print("������� �������� ������.\n")
                        while True:
                            product_name_to_delete = input("������� �������� ������ ��� �������� ��� 'back' ��� ����������� �����\n ")

                            if product_name_to_delete == 'back':
                                break

                            administrator.remove_product(product_name_to_delete)
                            print(f"����� '{product_name_to_delete}' ����� ������.\n")
                            break

                    elif administrator_action == '3':
                        print("������� ��������� �������� ������.\n")
                        while True:
                            product_name_to_change = input("������� �������� ������ ��� ��������� ��� 'back' ��� ����������� �����\n")

                            if product_name_to_change == 'back':
                                break

                            new_product_name = input("������� ����� �������� ������: ")
                            administrator.change_product_name(product_name_to_change, new_product_name)
                            print(f"�������� ������  �������� �� '{new_product_name}'.\n")
                            break

                    elif administrator_action == '4':
                        print("��  �����.\n")
                        break
            else:
                print("������������ ����� ��� ������. ���������� �����.\n")

    elif choice == '2':
        print("�����������\n")
        print("����� ������ ���� �� ����� 4 ��������\n")

        while True:
            login_client = input("���������� �����.\n")

            if len(login_client) >= 4:
                break
            else:
                print("����� ������ ��������� �� ����� 4 �������� � �� ������ ���� ������. ���������� �����.\n")

        while True:
            password_client = input("�������� ������.")

            if len(password_client) > 0:
                break
            else:
                print("���� '������' �� ����� ���� ������.\n")

        store.cursor.execute('SELECT * FROM users WHERE login = ?', (login_client,))
        existing_user = store.cursor.fetchone()

        if existing_user:
            print("������������ � ����� ������� ��� ����������. ���������� ������ �����.\n")
        else:

            hashed_password = bcrypt.hashpw(password_client.encode('utf-8'), bcrypt.gensalt())

            store.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login_client, hashed_password))

            store.conn.commit()

            print("����������� ���������.\n")
    elif choice == '3':
        print("��  �����.\n")
        break

    else:
        print("������������ ����. ���������� �����.\n")

store.close_connection()
