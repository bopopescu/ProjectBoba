from flask import Flask, render_template, request
from flaskext.mysql import MySQL
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'projectbobav2.cutrzyo9dvxs.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'boba'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Whyjustno123'
app.config['MYSQL_DATABASE_DB'] = 'two'
mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        bt = details['bobatexture']
        pr = details['price']
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from bobastoreNYC")
        data = cursor.fetchall()
        print(data)
        # cursor.execute("INSERT INTO bobastoreNYC(bobatexture, price) VALUES (%s, %d)", (bt, pr))
        # mysql.connection.commit()
        cursor.close()
        return "success"
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
