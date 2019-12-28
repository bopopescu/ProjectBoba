#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 14:17:04 2019

@author: khanhnguyen
"""

import requests 
import json
import mysql.connector


#### CONFIG #####
keys = {}
with open("key.json","r") as f:
    keys = json.loads(f.read())
    
API_key = keys["yelp_API"]
authorization = "Bearer " + API_key
NYU = "70 Washington Square Street New York, NY 10012"
url = "https://api.yelp.com/v3/businesses/search"
authorization = {"Authorization": authorization}

#### SETTING UP DB ####
db_user = keys['user']
db_pw = keys['password']

mydb = mysql.connector.connect(
  host="projectbobav2.cutrzyo9dvxs.us-east-1.rds.amazonaws.com",
  user=db_user,
  passwd=db_pw, 
  database="two"
)
cursor = mydb.cursor()

#Using yelp api to find bobastore
def find_bobastore(term):
    payload = {"term": term, "location": NYU, "categories": "bubbletea", "radius" : 1500}
    results = results.get(url, params = payload, headers = authorization)

#find bobastore in database, if not exist, find using Yelp API
def find_bobastore_db(conn, term):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bobastoreNYC WHERE storename = %{name}s", {"name": term})
    data = cursor.fetchall()
    if len(data) == 0:
        data = find_bobastore(term)
    return data

#Check if a store exists in the database
def check_exist(cursor, storename):
    sql = "SELECT * FROM bobastoreNYC WHERE storename = %(bobastore)s"
    cursor.execute(sql, {"bobastore": storename})
    data = cursor.fetchall()
    if(len(data) > 0):
        return True
    return False


# Quick script to insert some more bobastore into the database
#payload = {"location": NYU, "categories": "bubbletea"}
#results = requests.get(url, params = payload, headers = authorization)
#businesses = json.loads(results.content)['businesses']
#for business in businesses:
#    if check_exist(cursor, business['name']) is False:
#        address = business['location']['display_address'][0] + ', ' + business['location']['display_address'][1]
#        store = (business['name'], address, business['display_phone'])
#        print(store)
#        sql = "INSERT INTO bobastoreNYC (storename, storeaddress, phone) VALUES (%s, %s, %s)"
#        cursor.execute(sql, store)
#        mydb.commit()
#        
#cursor.close()
#mydb.close()

