import mysql.connector
import configparser

try:
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    host = config['DEFAULT']['db_host']
    user = config['DEFAULT']['db_user']
    password = config['DEFAULT']['db_password']
    database = config['DEFAULT']['db_name']
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="timesheet"
    )
except:
    print("Some problem in db_config.ini")


# setting up connection
def connect(): 
    # connection = sqlite3.connect("_set.db")   
    try: 
        return connection
    except NameError: 
        print ("Failed to connect to database")
     

def fetch(query,*args): 
    try:       
        cursor = connect().cursor()        
    except:
        print ("****Fetch Query Failed!**** Failed to connect to database")
        return
    if len(*args)>0:
        cursor.execute(query, *args)
        result = cursor.fetchall()                
    else:
        cursor.execute(query)
        result = cursor.fetchall()             
    return result

def update(query,*args):  
    try:       
        cursor = connect().cursor()
    except:
        print ("****Update Query Failed!**** Failed to connect to database")
        return    
    cursor.execute(query,*args)
    connection.commit() 

def insert(query,*args): 
    try:       
        cursor = connect().cursor()
    except:
        print ("****Insert Query Failed!**** Failed to connect to database")
        return       
    cursor.execute(query,*args)
    connection.commit()    

def delete(query,*args): 
    try:       
        cursor = connect().cursor()
    except:
        print ("****Delete Query Failed!**** Failed to connect to database")
        return      
    cursor.execute(query,*args)
    connection.commit()    

