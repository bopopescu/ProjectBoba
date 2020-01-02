from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json
import handlers

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
        data = handlers.matching(conn, boba_texture, price, bobatype)
        conn.close()
        return render_template("search.html", outputdata = data, searched = True)
    return render_template("search.html")


@app.route("/table", methods=['GET', 'POST'])
def table():
    conn = create_connection()
    tabledata = handlers.getAll(conn)
    if request.method == "POST":
        details = request.form
        storename= details['storename']
        reason = details['reason']
        bobatexture = details['bobatexture']
        addition = handlers.addRec(conn, storename, reason, bobatexture)
        conn.close()
        return render_template("table.html", table = tabledata, result = addition)
    conn.close()
    return render_template("table.html", table = tabledata)



if __name__ == "__main__":
    app.run()
