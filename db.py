import sqlite3
from sqlite3 import Error
import  os
import requests
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
        cursor.close()

        conn.close()
        
    except Exception as e:
        print(e)
        cursor.close()

        conn.close()

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
                "UID":list(rows[0])[0],
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

def addMoie(movie=None):
    if movie == None:
        return None
    else:
        try:
            title = movie["title"]
            overview = movie['overview']
            adult = movie['adult']
            status = movie['status']
            release_date = movie['release_date']
            imdb_id = movie['imdb_id']
            tmdb_id = movie['id']
            tagline = movie['tagline']
            

            poster_path = movie['poster_path']
            backdrop_path = movie['backdrop_path']

            if poster_path is not None:
                posterBlob = get_image(poster_path)
                print("Downloaded Image Data:" , type(posterBlob))

            if backdrop_path is not None:
                backdropBlob =  get_image(backdrop_path)
                print("Downloaded Image Data:" , type(backdropBlob))

            qry = ''' INSERT INTO movies(title,overview,adult,status,release_date,imdb_id,tmdb_id,backdrop,poster,tagline)
                VALUES(?,?,?,?,?,?,?,?,?,?) '''

            data = (title,overview,adult,status,release_date,imdb_id,tmdb_id,backdropBlob,posterBlob,tagline)

            conn = create_connection()
            cur = conn.cursor()
            cur.execute(qry,data)
            conn.commit()
            cur.close()
            conn.close()
            return [0,"Data added Success Full"]
        except sqlite3.IntegrityError as err:
            print(err)
            return [1,err]

            

def get_image(image_path):
    try:
       
        # url = f'http://image.tmdb.org/t/p/original/{poster_path}'
        url = f'http://image.tmdb.org/t/p/w500/{image_path}'
        r = requests.get(url, allow_redirects=True)

        if r.status_code == 200:
            
            return r.content
        else:
            blob = convertToBinaryData("poster_placeholder_light.png")
            return blob
    except :
        blob = convertToBinaryData("poster_placeholder_light.png")
        return blob
    

if not os.path.exists(db_location):
    print("creating db")
    init()
else:
    print("db already exits")

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData