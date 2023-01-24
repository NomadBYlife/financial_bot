import datetime
import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('bot_db.db',
                    detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, name TEXT, nick_name TEXT)
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (item TEXT, amount INT, date_main TEXT, description TEXT, user INT, foreign key (user) references users (user_id))
        """)


async def create_user(user_id, name, nick_name):
    user = cur.execute("""
        SELECT 1 FROM users WHERE user_id == '{user_id}'
    """.format(user_id=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users(user_id, name, nick_name) VALUES ('{user_id}','{name}','{nick_name}')".format(
            user_id=user_id, name=name, nick_name=nick_name))
        db.commit()


async def edit_expenses(state):
    async with state.proxy() as data:
        cur.execute(
            f"INSERT INTO expenses(item, amount, description, user, date_main) VALUES ('{data['item']}', '{data['amount']}',"
            f" '{data['description']}', '{data['user_id']}', date('now'))"
        )
        db.commit()


async def get_general_data(user_id: dict):
    data = cur.execute("SELECT * FROM expenses WHERE user == '{}' ORDER BY date_main".format(user_id)).fetchall()
    return data


async def get_data_current_month(user_id: dict):
    data = cur.execute(
        f"SELECT * FROM expenses WHERE user == '{user_id}' and date_main BETWEEN date('now','start of month') and date('now') ORDER BY date_main").fetchall()
    return data

async def get_data_choosen_month(user_id: dict, data: dict):
    if len(data['month']) < 2:
        date_start = f"20{data['year']}-0{data['month']}-01"
        date_finish = f"20{data['year']}-0{data['month']}-31"
    else:
        date_start = f"20{data['year']}-{data['month']}-01"
        date_finish = f"20{data['year']}-{data['month']}-31"
    data = cur.execute(
        """SELECT * FROM expenses WHERE user == '{}' and date_main BETWEEN date('{}') and date('{}')""".format(user_id, date_start, date_finish)).fetchall()
    return data
