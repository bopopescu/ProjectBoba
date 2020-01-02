#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 14:17:04 2019

@author: khanhnguyen
"""

import requests 
import json
import mysql.connector

#Quick script to insert more bobastores into the db

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
