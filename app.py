from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json

##### CONFIG #####
app = Flask(__name__)

#Retrieve username and password from json
keys = {}
with open("key.json","r") as f:
    keys = json.loads(f.read())

db_user = keys['user']
db_pw = keys['password']

app.config['MYSQL_DATABASE_HOST'] = 'projectbobav2.cutrzyo9dvxs.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = db_user
app.config['MYSQL_DATABASE_PASSWORD'] = db_pw
app.config['MYSQL_DATABASE_DB'] = 'two'
mysql = MySQL(app)


#Create_connection
def create_connection():
    conn = None
    try:
        conn = mysql.connect()
    except Exception as e:
        print(e)
    return conn

#Select values from a database
def select_values(sql, cursor):
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
    except:
        cursor.close()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        bt = details['bobatexture']
        pr = details['price']
        conn = create_connection()
        cursor = conn.cursor()
        data = select_values("SELECT * FROM bobastoreNYC", cursor)
        print(data)
        # cursor.execute("INSERT INTO bobastoreNYC(bobatexture, price) VALUES (%s, %d)", (bt, pr))
        # mysql.connection.commit()
        cursor.close()
        conn.close()
        return "success"
    return render_template("index.html")


if __name__ == "__main__":
    app.run()

