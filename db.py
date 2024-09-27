from shifr import hash_data, encrypt, decrypt, decrypt_data


def data_output_title(cursor, username, title):
    data_from_db = data_output(cursor, username)
    data = decrypt_data(data_from_db)
    for i in range(len(data)):
        if data[i][2] == title:
            return data[i]


def data_output(cursor, username):
    username = hash_data(username)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
    row = cursor.fetchall()

    return row


def entering_data(cursor, username, title, login, password):
    username, title, login, password = hash_data(username), encrypt(title), encrypt(login), encrypt(password)

    cursor.execute(f"INSERT INTO users (username, title, login, password) "
                   f"VALUES ('{username}', '{title}', '{login}', '{password}');")


def entering_data_temporary(cursor, username, title, login, password):
    username, title, login, password = hash_data(username), encrypt(title), encrypt(login), encrypt(password)
    cursor.execute(f"INSERT INTO temporary (username, title, login, password) "
                   f"VALUES ('{username}', '{title}', '{login}', '{password}');")


def full_delete_data(cursor, username):
    username = hash_data(username)
    cursor.execute(f"DELETE FROM users WHERE username = '{username}';")


def delete_data(cursor, username, title):
    data = data_output_title(cursor, username, title)
    cursor.execute(f"DELETE FROM users WHERE id = {data[0]};")


def update_data(cursor, username):
    cursor.execute(f"SELECT * FROM temporary WHERE username = '{hash_data(username)}';")

    data_from_db = cursor.fetchone()
    title = decrypt(data_from_db[2])
    data = data_output_title(cursor, username, title)

    cursor.execute(f"UPDATE users SET login = '{data_from_db[3]}', password = '{data_from_db[4]}' "
                   f"WHERE id = {data[0]};")

    delete_temporary(cursor, username)


def delete_temporary(cursor, username):
    username = hash_data(username)
    cursor.execute(f"DELETE FROM temporary WHERE username = '{username}';")


def availability(cursor, username):
    username = hash_data(username)
    cursor.execute(f"SELECT active_func FROM polzovateli WHERE username = '{username}';")
    row = cursor.fetchone()
    return row


def add_polzovatel(cursor, username):
    username = hash_data(username)
    cursor.execute(f"SELECT * FROM polzovateli WHERE username = '{username}';")
    row = cursor.fetchone()

    if row is None:
        count = count_account(cursor, username)
        cursor.execute(f"INSERT INTO polzovateli (username, count_account, active_func, podpiska) "
                       f"VALUES ('{username}', {count[0]}, 'account', false);")


def count_account(cursor, username):
    cursor.execute(f"SELECT COUNT(users.username) AS kolichestvo FROM users WHERE username = '{username}';")
    row = cursor.fetchone()
    return row
