from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json
import time
import datetime

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

#Matching results based on boba_texture, bobatype and price
def matching(cursor, boba_texture, price, bobatype):
    try:
        cursor.execute(f"SELECT * FROM bobastoreNYC WHERE \
                       bobatexture = %(boba_texture)s AND price = %(price)s AND {bobatype} = 1",
                       {"boba_texture": boba_texture, "price": price})
        data = cursor.fetchall()
        return data
    except:
        cursor.close()

def addRec(conn, cursor, storename, reason, bobatexture):
    try:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO recommendation (storename,  bobatexture, \
                        reason, submittime) VALUES(%(storename)s, \
                        %(bobatexture)s, %(reason)s, %(timestamp)s)",
                       {"storename": storename, "reason": reason, \
                        "timestamp": timestamp, 'bobatexture': bobatexture})
        conn.commit()
        return "success"
    except:
        cursor.close()
        return "failed"

def getAll(cursor):
    try:
        cursor.execute("SELECT storename, storeaddress, whatwelike FROM bobastoreNYC")
        data = cursor.fetchall()
        return data
    except:
        cursor.close()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        details = request.form
        boba_texture = details['bobatexture']
        price = details['price']
        bobatype = details['bobatype']
        conn = create_connection()
        cursor = conn.cursor()
        data = matching(cursor, boba_texture, price, bobatype)
        cursor.close()
        conn.close()
        return render_template("search.html", outputdata = data, searched = True)
    return render_template("search.html")


@app.route("/table", methods=['GET', 'POST'])
def table():
    conn = create_connection()
    cursor = conn.cursor()
    tabledata = getAll(cursor)
    if request.method == "POST":
        details = request.form
        storename= details['storename']
        reason = details['reason']
        bobatexture = details['bobatexture']
        addition = addRec(conn, cursor, storename, reason, bobatexture)
        cursor.close()
        conn.close()
        return render_template("table.html", table = tabledata, result = addition)
    cursor.close()
    conn.close()
    return render_template("table.html", table = tabledata)


if __name__ == "__main__":
    app.run()
