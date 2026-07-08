import os
import hashlib
import time
import mysql.connector
from datetime import datetime
from db_config import db_config

# Corrected file path
file_name = r"C:\\Users\\shrav\\OneDrive\\Desktop\\Project\\info.txt"

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def db_change(file_path, old_hash, new_hash, change_type):
    connect = None
    try:
        connect = mysql.connector.connect(**db_config)
        cursor = connect.cursor()
        query = """INSERT INTO file_change(file_path, old_hash, new_hash, change_type) 
                   VALUES (%s, %s, %s, %s)"""
        
        cursor.execute(query, (file_path, old_hash, new_hash, change_type))
        connect.commit()
    
    except mysql.connector.Error as err:
        print(f"ERROR!! {err}")
    
    finally:
        if connect and connect.is_connected():
            cursor.close()
            connect.close()

initial_hash = calculate_hash(file_name)

while True:
    time.sleep(10)  
    current_hash = calculate_hash(file_name)
    
    if current_hash != initial_hash:
        print(f"File {file_name} has been modified.")
        db_change(file_name, initial_hash, current_hash, 'MODIFIED')
        initial_hash = current_hash  # Update the hash to the new value
        
    
    
    


        
        
    