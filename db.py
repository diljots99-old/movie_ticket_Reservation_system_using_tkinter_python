import sqlite3
from sqlite3 import Error
import  os

current_dir = os.getcwd()
db_location = current_dir + "\sqllite.db"
print(db_location)


def create_connection(db_file=db_location):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def init():
    conn = create_connection()

    qry = open('movie.sql', 'r').read()
    c = conn.cursor()
    sqlite3.complete_statement(qry)
    cursor = conn.cursor()
    try:
        cursor.executescript(qry)
    except Exception as e:
        print(e)
        cursor.close()
        raise


def auth_user(email,password):
    try:
        qry = "SELECT * FROM 'users' WHERE (username == '{}' OR email == '{}') AND  password == '{}';".format(email,email,password)
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(qry)
        rows = cur.fetchall()
        
        if len(rows)==1:
            print("User Exists")
            userdetails = {
                "Sr. No":list(rows[0])[0],
                "username":list(rows[0])[1],
                "password":list(rows[0])[2],
                "email":list(rows[0])[3],
                "privilege":list(rows[0])[4]
            }
            return ["success",userdetails]
        if len(rows) == 0:
            print("user does not exits")
            return None
    except :
        return None

    

if not os.path.exists(db_location):
    print("creating db")
    init()
else:
    print("db already exits")