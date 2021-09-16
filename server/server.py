from bottle import Bottle, route, run, post, get, request, static_file, template, response
from query import fetch, update, insert, delete
import collections
import requests
import json
import random
import binascii
import hmac
import hashlib
from datetime import date
import datetime




### API SECTION ###
@route('/login', method='POST')
def login_api():   
    handlingHeaders()
    Email  = request.forms.get('email', None)
    Password = request.forms.get('password', None)  
    hashedPwd = hmac.new( b'am@xza', msg=str.encode(Password), digestmod=hashlib.sha256) 
    Password = hashedPwd.hexdigest()    
    sql = 'SELECT * FROM users WHERE email = %s AND password = %s '
    result = fetch(sql,(Email,Password,)) 
    result = toJson(result,["id","name","email","designation","contact","password"])   
          
    #Check if user with credentials exsists
    if len(result)>0:
        user_id = (result[0]['id'])
        email = (result[0]['email'])
        hashedToken = hmac.new( b'am@xza', msg=str.encode(email), digestmod=hashlib.sha256)
        Token = hashedToken.hexdigest()
        sql = 'SELECT * FROM sessions WHERE uid = %s '
        result = fetch(sql,(user_id,)) 
        #Check if user already has session
        if len(result)>0:            
            sql = '''UPDATE sessions SET token = %s WHERE uid = %s '''
            result = update(sql,(Token, user_id,)) 
        else:                               
            sql = '''INSERT INTO sessions (token,uid) VALUES(%s, %s)'''
            result = insert(sql,(Token, user_id,))     
        return {"success":"1", "token":Token}
    else:
        return {"success":"0", "token":"", "msg":"Invalid Credentials"} 


@route('/permissionGet', method=['OPTIONS','GET'])
def permission_get():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            return {"success":"1", "type":"0"}  #Type 0 means admin privileges
        elif(verifyToken(Auth)["verified"]):
            return {"success":"1", "type":"1"}  #Type 1 means user privileges 
        else:    
            return {"success":"0", "msg":"Session expired"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}


@route('/getUsers', method=['OPTIONS','GET'])  
def get_users():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"]):
            sql = 'SELECT * FROM users'
            result = fetch(sql,())    
            result = toJson(result,["id","name","email","designation","contact","password"])             
            return json.dumps({"success":"1", "data":result})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}
 
@route('/getUser', method=['OPTIONS','POST'])  
def get_user():
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            Uid  = request.forms.get('uid', None)
            sql = 'SELECT * FROM users WHERE id = %s'
            result = fetch(sql,(Uid,))    
            result = toJson(result,["id","name","email","designation","contact","password"])             
            return json.dumps({"success":"1", "data":result})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}    

@route('/addUser', method=['OPTIONS','POST']) 
def add_user():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")   
    if(Auth):              
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            Email  = request.forms.get('email', None)
            Name = request.forms.get('name', None)  
            Designation = request.forms.get('designation', None)  
            Contact = request.forms.get('contact', None) 
            Password = request.forms.get('password', None)             
            hashedPwd = hmac.new( b'am@xza', msg=str.encode(Password), digestmod=hashlib.sha256)
            Password = hashedPwd.hexdigest()  
            sql = 'INSERT INTO users (name,email,designation,contact,password) VALUES (%s,%s,%s,%s,%s)'
            insert(sql,(Name,Email,Designation,Contact,Password))                
            return {"success":"1", "msg":""}
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}

@route('/editUser', method=['OPTIONS','POST']) 
def edit_user():
    handlingHeaders()
    Auth = request.headers.get("Authorization") 
    if(Auth):
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):  
            Uid  = request.forms.get('uid', None)
            Email  = request.forms.get('email', None)
            Name = request.forms.get('name', None)  
            Designation = request.forms.get('designation', None)  
            Contact = request.forms.get('contact', None) 
            Password = request.forms.get('password', None) 
            if Password == None:            
                sql = '''   UPDATE users 
                            SET name = %s, email = %s, designation = %s, contact = %s 
                            WHERE id = %s
                    '''
                update(sql,(Name,Email,Designation,Contact, Uid)) 
            else:    
                hashedPwd = hmac.new( b'am@xza', msg=str.encode(Password), digestmod=hashlib.sha256)
                Password = hashedPwd.hexdigest()  
                sql = '''   UPDATE users 
                            SET name = %s, email = %s, designation = %s, contact = %s, password = %s  
                            WHERE id = %s
                    '''
                update(sql,(Name,Email,Designation,Contact,Password, Uid)) 
            return {"success":"1", "msg":""}    
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}   



@route('/getProjects', method=['OPTIONS','GET'])  
def get_projects():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            sql = '''
                    SELECT 
                    p.id, 
                    p.name,
                    DATE_FORMAT(p.start_date, '%Y/%m/%d') AS start_date, 
                    DATE_FORMAT(p.end_date, '%Y/%m/%d') AS end_date,         
                    CASE p.status
                        WHEN 1 THEN "On going"
                        WHEN 2 THEN "On Hold"
                        WHEN 3 THEN "Closed"
                    END AS status
                    FROM projects AS p                   
                '''
            result = fetch(sql,()) 
            result = toJson(result,["id","name","start_date","end_date","status"])              
            return json.dumps({"success":"1", "data":result})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}
 
@route('/getProject', method=['OPTIONS','POST'])  
def get_project():
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            Pid  = request.forms.get('pid', None)
            sql = '''
                    SELECT 
                    p.id, 
                    p.name,
                    DATE_FORMAT(p.start_date, '%Y/%m/%d') AS start_date, 
                    DATE_FORMAT(p.end_date, '%Y/%m/%d') AS end_date,      
                    p.status
                    FROM projects AS p 
                    WHERE p.id = %s
                '''
            result = fetch(sql,(Pid,))    
            result = toJson(result,["id","name","start_date","end_date","status"])             
            return json.dumps({"success":"1", "data":result})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}    

@route('/addProject', method=['OPTIONS','POST']) 
def add_project():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")   
    if(Auth):              
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            Name  = request.forms.get('name', None)
            Start_Date = request.forms.get('start_date', None)  
            End_Date = request.forms.get('end_date', None)  
            Status = request.forms.get('status', None)            
            sql = '''
                        INSERT INTO projects 
                        (name,start_date,end_date,status) 
                        VALUES 
                        (%s,%s,%s,%s)
                    '''
            insert(sql,(Name,Start_Date,End_Date,Status))                
            return {"success":"1", "msg":""}
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}

@route('/editProject', method=['OPTIONS','POST']) 
def edit_project():
    handlingHeaders()
    Auth = request.headers.get("Authorization") 
    if(Auth):
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):  
            Pid  = request.forms.get('pid', None)
            Name  = request.forms.get('name', None)
            Start_Date  = request.forms.get('start_date', None)
            End_Date = request.forms.get('end_date', None)  
            Status = request.forms.get('status', None)                                
            sql = '''   UPDATE projects 
                        SET name = %s, 
                        start_date = %s, 
                        end_date = %s,  
                        status = %s 
                        WHERE id = %s
                '''
            update(sql,(Name,Start_Date,End_Date,Status, Pid))           
            return {"success":"1", "msg":""}    
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}   


@route('/getTimesheets', method=['OPTIONS','POST'])  
def get_timesheets():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"]):
            Page = request.forms.get('page', None) 
            Page = (int(Page)-1)*30                                              
            sql = '''
                        SELECT 
                            S.id as id,
                            U.name AS employee, 
                            S.date as date, 
                            COUNT(T.id) as total_tasks, 
                            SUM(T.hours)as total_hours
                        FROM 
                            users AS U,  sheet AS S, task AS T
                        WHERE
                            U.id = S.uid
                        AND
                            T.sid = S.id 
                        GROUP BY 
                            S.id , S.date   
                        ORDER BY
                            S.date DESC 
                        LIMIT   30 
                        OFFSET %s                 
                    '''         
            result = fetch(sql,(Page,))         
            result = toJson(result,["id","employee","date","total_tasks","total_hours"])             
            return json.dumps({"success":"1", "data":result})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}

@route('/initTimesheet', method=['OPTIONS','GET']) 
def init_sheet():
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"]):
            sql = '''
                    SELECT 
                    p.id, 
                    p.name             
                    FROM projects AS p      
                    WHERE p.status in (1,2)            
                '''
            result = fetch(sql,()) 
            result = toJson(result,["id","name",])              
            today = str(date.today())
            data = {"projects": result, "date":today }            
            return ({"success":"1", "data":data})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}

@route('/newSheet', method=['OPTIONS','POST']) 
def new_sheet():
    handlingHeaders()
    Auth = request.headers.get("Authorization") 
    if(Auth):
        if(verifyToken(Auth)["verified"]):
            Tasks  = request.forms.get('tasks', [])
            Date  = request.forms.get('date', "")
            Tasks = json.loads(Tasks)
            #Convert Date to MySQL Format#
            d = datetime.datetime.strptime(Date, '%Y-%m-%d')
            d = datetime.date.strftime(d, "%Y/%m/%d")
            Date = str(d)
            #Check if User has already submitted a sheet#
            sql = '''SELECT uid FROM sessions WHERE token = %s'''
            result = fetch(sql,(Auth,))
            result = toJson(result,["uid",])  
            Uid = result[0]['uid']
            sql = '''SELECT * FROM sheet WHERE uid = %s AND date = %s '''
            result = fetch(sql,(Uid,Date))
            result = toJson(result,["id","uid","date"]) 
            #Proceed if the sheet for the same date doesn't exist
            try:
                if len (result) < 1:
                    sql = '''INSERT INTO sheet (uid, date) VALUES (%s,%s)'''
                    insert(sql,(Uid,Date,))     
                    sql = '''SELECT MAX(id) as max_id FROM sheet'''
                    result = fetch(sql,())
                    result = toJson(result,["max_id",])            
                    Sid = result[0]['max_id']
                    BulkInsertValues=""                
                    for task in Tasks:
                        BulkInsertValues = BulkInsertValues+ '("'+task['name']+ '",' +str(Sid)+ ',' +str(task['pid'])+ ',' +str(task['hours'])+ ',' +str(task['status'])+ ',"' +task['comment']+'."'+ '),'
                    BulkInsertValues =  BulkInsertValues[:-1]
                    sql = '''INSERT INTO task(name,sid,pid,hours,status,comment) VALUES '''+BulkInsertValues                    
                    insert(sql,())                
                    return {"success":"1", "msg":""}
            except Exception as E:
                print("****ERROR****\n", E)
                return {"success":"0", "msg":"Process failed, Error occurred at server end"}
                                
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}


#-------------Helper Functions ----------------#
def verifyToken(token):    
    sql = '''SELECT * FROM sessions WHERE token = %s'''
    result = fetch(sql,(token,))    
    result = toJson(result,["id","uid","token"])     
    if len(result) > 0 and result[0]['uid'] == 0:
        return({"verified":True, "isAdmin":True})
    elif len(result)>0:
        return({"verified":True, "isAdmin":False})  
    else :
        return({"verified":False, "isAdmin":False})       

def toJson(result,keys):
    objects_list = []
    for row in result: 
        d = {}
        for index,item in enumerate (row, start=0):                                    
            d[keys[index]] = item      
        objects_list.append(d)
    return (objects_list)

def handlingHeaders():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Content-Type", "application/json")
    response.set_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST")
    response.set_header("Access-Control-Allow-Headers","Origin, X-Requested-With, Content-Type, Accept, Authorization")



#------------- Importing Resources For HTML ----------------#

@get("/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="")

@get("/<filepath:re:.*\.svg>")
def svg(filepath):
    return static_file(filepath, root="./")

@get("/<filepath:re:.*\.(jpg|png|gif|ico)>")
def img(filepath):
    return static_file(filepath, root="./")

@get("/<filepath:re:ReactClientbundle.js>")
def js(filepath):
    return static_file(filepath, root="")
    
@get("/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="")

@get("/<filepath:re:.*\.(woff|woff2|ttf)>")
def js(filepath):
    return static_file(filepath, root="../")


run(host='0.0.0.0', server="waitress", port=4040)
