import mysql.connector
import json


# This is to test the data science part.
#***REMOVE WHEN DEPLOY***

keys = {}
with open("key.json","r") as f:
    keys = json.loads(f.read())

db_user = keys['user']
db_pw = keys['password']

mydb = mysql.connector.connect(
  host="projectbobav2.cutrzyo9dvxs.us-east-1.rds.amazonaws.com",
  user=db_user,
  passwd=db_pw,
  database="two"
)
cursor = mydb.cursor()

# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# cursor.execute(sql, val)
# mydb.commit()

sql = "SELECT * FROM bobastoreNYC"
cursor.execute(sql)
data = cursor.fetchall()

print(data)
