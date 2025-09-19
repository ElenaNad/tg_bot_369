import sqlite3 as sl


def create_connection(db_file):
    conn = sl.connect(db_file, check_same_thread=False)
    cursor = conn.cursor()
    return cursor, conn


def add_table_w(conn):
    with conn:
        conn.execute('''
CREATE TABLE IF NOT EXISTS weight_history (
    user_id STRING,
    weight FLOAT,
    date STRING
)
''')


def create_connection_w(db_file):
    conn_w = sl.connect(db_file, check_same_thread=False)
    cursor_w = conn_w.cursor()
    return cursor_w, conn_w


def insert_id_w(cur, id):
    sql = 'INSERT INTO weight_history (user_id, weight, date) VALUES (?, ?, ?)'
    cur.execute(sql, (id, None, None))
    cur.connection.commit()


def insert_weight_w(cur, weight, id, date):
    sql = ('INSERT INTO weight_history (user_id, weight, date) VALUES (?, ?, ?)')
    cur.execute(sql, (id, weight, date))
    cur.connection.commit()


def add_table(conn):
    with conn:
        conn.execute(
            'CREATE TABLE IF NOT EXISTS users (id STRING PRIMARY KEY, name VARCHAR(100), age INT, weight FLOAT, height INT);')


def insert_id(cur, id):
    sql = 'INSERT INTO users (id, name, age, height, weight) VALUES (?, ?, ?, ?, ?)'
    cur.execute(sql, (id, None, None, None, None))
    cur.connection.commit()


def insert_name(cur, id, name):
    sql = 'UPDATE users SET name = ? WHERE id = ?'
    cur.execute(sql, (name, id))
    cur.connection.commit()


def insert_age(cur, id, age):
    sql = 'UPDATE users SET age = ? WHERE id = ?'
    cur.execute(sql, (age, id))
    cur.connection.commit()


def insert_weight(cur, id, weight):
    sql = 'UPDATE users SET weight = ? WHERE id = ?'
    cur.execute(sql, (weight, id))
    cur.connection.commit()


def insert_height(cur, id, height):
    sql = 'UPDATE users SET height = ? WHERE id = ?'
    cur.execute(sql, (height, id))
    cur.connection.commit()


def del_data(cur, id):
    sql = f'DELETE FROM users WHERE id = ?'
    cur.execute(sql, (id,))
    cur.connection.commit()


def del_data_w(cur, id):
    sql = f'DELETE FROM weight_history WHERE user_id = ?'
    cur.execute(sql, (id,))
    cur.connection.commit()


def get_user(cur, id):
    sql = "SELECT * FROM users WHERE id = ?"
    user = cur.execute(sql, (id,)).fetchone()
    if user:
        return user, True
    else:
        return "Пользователь не найден", False


def get_name(cur, id):
    sql = "SELECT name FROM users WHERE id = ?"
    return cur.execute(sql, (id,)).fetchone()[0]


def get_age(cur, id):
    sql = "SELECT age FROM users WHERE id = ?"
    return cur.execute(sql, (id,)).fetchone()[0]


def get_height(cur, id):
    sql = "SELECT height FROM users WHERE id = ?"
    return cur.execute(sql, (id,)).fetchone()[0]


def get_weight(cur, id):
    sql = "SELECT weight FROM users WHERE id = ?"
    return cur.execute(sql, (id,)).fetchone()[0]


def get_user_data(cur, id):
    return f"Ваши данные: \n Имя: {get_name(cur, id)} \n Возраст: {get_age(cur, id)} \n Рост: {get_height(cur, id)} \n Вес: {get_weight(cur, id)}"


def check_user_data(cur, id):
    data = get_user(cur, id)
    if data[1]:
        if all(data[0]):
            return "Все поля заполнены"
        sentence = "Не заполнены: "
        if data[0][1] == None:
            sentence += "Имя, "
        if data[0][2] == None:
            sentence += "Возраст, "
        if data[0][3] == None:
            sentence += "Вес, "
        if data[0][4] == None:
            sentence += "Рост, "
        return sentence[:-2] + "."
    return "Пользователь не найден"


def get_weight_data(cur, id):
    sql = "SELECT weight, date FROM weight_history WHERE user_id = ?"
    data = cur.execute(sql, (id,)).fetchall()
    if data:
        new_data = []
        for elem in data:
            new_data.append(f"Вес: {elem[0]}, Дата: {elem[1]}")
        sentence = f"История веса:\n{"\n".join(new_data)}"
        return sentence

    else:
        return "Пользователь не найден"


if __name__ == "__main__":
    database = 'users.db'
    database1 = 'weight_history.db'
    cursor, connection = create_connection(database)
    cursor_w, connection_w = create_connection_w(database1)
    add_table(connection)
    add_table_w(connection_w)
    connection.close()
    connection_w.close()
