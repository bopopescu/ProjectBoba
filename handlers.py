#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 23:30:19 2020

@author: khanhnguyen
"""
#Script handling business logic 

import time
import datetime
import bcrypt

ts = time.time()
#Matching results based on boba_texture, bobatype and price. 
#@TODO:Boba type is at 1 right now. Should change later accordingly
def matching(conn, boba_texture, price, bobatype):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM bobastoreNYC WHERE \
                       bobatexture = %(boba_texture)s AND price = %(price)s AND {bobatype} = 1",
                       {"boba_texture": boba_texture, "price": price})
        data = cursor.fetchall()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"INSERT INTO searchdata (bobatexture, price, {bobatype}, submittime) \
                        VALUES(%(bobatexture)s, %(price)s, 1, %(timestamp)s)",
                       {'bobatexture': boba_texture, 'price': price, 'timestamp':timestamp})
        conn.commit()
        cursor.close()
        return data
    except Exception as e:
        print(e)
        cursor.close()
        return "failed"

#Add recommendation to the database
#@TODO: Add column to say who describes the boba texture is chewy or soft or regular        
def addRec(conn, storename, reason, bobatexture):
    try:
        cursor = conn.cursor()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO recommendation (storename,  bobatexture, \
                        reason, submittime) VALUES(%(storename)s, \
                        %(bobatexture)s, %(reason)s, %(timestamp)s)",
                       {"storename": storename, "reason": reason, \
                        "timestamp": timestamp, 'bobatexture': bobatexture})
        conn.commit()
        cursor.close()
        return "success"
    except Exception as e:
        print(e)
        cursor.close()
        return "failed"

#Get all the bobastores in the database
def getAll(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT storename, storeaddress, whatwelike FROM bobastoreNYC")
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print(e)
        cursor.close()
        return "failed"

#Hashing password using bcrypt
def hash_password(plain_password):
    return bcrypt.hashpw(plain_password, bcrypt.gensalt())

#Checking password using bcrypt
def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password, hash_password)

def insertUser(conn, username, password):
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO user (username, password) VALUES \
                       (%(username)s, %(hashed_password))", 
                       {"username": username, "hashed_password": hashed_password})
        conn.commit()
        cursor.close()
        return "success"
    except Exception as e:
        print(e)
        cursor.close()
        return "failed"
    