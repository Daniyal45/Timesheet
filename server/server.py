from bottle import Bottle, route, run, post, get, request, static_file, template, response
from query import fetch, update, insert, delete
import os
import json
import hmac
import hashlib
from datetime import date
import datetime
import time
import math
from io import BytesIO
from bottle import route, response
from pandas import ExcelWriter, DataFrame


@route('/', method='GET')
def home():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    return template('./index')


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
        designation = (result[0]['designation'])
        email = (result[0]['email'])
        Time = time.time()
        hashedToken = hmac.new( b'am@xza', msg=str.encode(email), digestmod=hashlib.sha256)
        Token = hashedToken.hexdigest()
        sql = 'SELECT * FROM sessions WHERE uid = %s '
        result = fetch(sql,(user_id,)) 
        #Check if user already has session
        if len(result)>0:            
            sql = '''UPDATE sessions SET token = %s, timestamp = %s, designation = %s WHERE uid = %s '''
            result = update(sql,(Token, Time, designation, user_id )) 
        else:                               
            sql = '''INSERT INTO sessions (token, uid, designation, timestamp) VALUES(%s, %s, %s, %s)'''
            result = insert(sql,(Token, user_id,designation,Time))     
        return {"success":"1", "token":Token}
    else:
        return {"success":"0", "token":"", "msg":"Invalid Credentials"} 


@route('/permissionGet', method=['OPTIONS','GET'])
def permission_get():       
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):
            Name = getLoggedInUserName(Auth)
            return {"success":"1", "type":"0", "user": Name }  #Type 0 means admin privileges
        elif(verifyToken(Auth)["verified"]):
            Name = getLoggedInUserName(Auth)
            return {"success":"1", "type":"1", "user": Name }  #Type 1 means user privileges 
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
            PerPage = 30
            Page = request.forms.get('page', None) 
            Page = (int(Page)-1)*PerPage            
            User_id_condition = ''' '''
            if verifyToken(Auth)["uid"] is not None and verifyToken(Auth)["uid"]>0:
                User_id_condition = " AND S.uid = " +  str(verifyToken(Auth)["uid"])  + " "   
            sql = '''
                        SELECT 
                            S.id as id,
                            U.name AS employee, 
                            S.date as date, 
                            COUNT(T.id) as total_tasks, 
                            SUM(T.hours)as total_hours,
                            COUNT(S.id)as total_sheets
                        FROM 
                            users AS U,  sheet AS S, task AS T
                        WHERE
                            U.id = S.uid
                        AND
                            T.sid = S.id 
                        ''' + User_id_condition + '''    
                        GROUP BY 
                            S.id , S.date   
                        ORDER BY
                            S.date DESC                                                
                    '''               
                     
            result = fetch(sql,())
            Total_Pages = math.ceil(len(result)/PerPage)       

            sql = '''
                        SELECT 
                            S.id as id,
                            U.name AS employee, 
                            S.date as date, 
                            COUNT(T.id) as total_tasks, 
                            SUM(T.hours)as total_hours,
                            COUNT(S.id)as total_sheets
                        FROM 
                            users AS U,  sheet AS S, task AS T
                        WHERE
                            U.id = S.uid
                        AND
                            T.sid = S.id 
                        ''' + User_id_condition + '''    
                        GROUP BY 
                            S.id , S.date   
                        ORDER BY
                            S.date DESC 
                        LIMIT ''' + str(PerPage) + ''' 
                        OFFSET %s  
                    '''               
                     
            result = fetch(sql,(Page,))         
            result = toJson(result,["id","employee","date","total_tasks","total_hours","total_sheets"])             
            return json.dumps({"success":"1", "data":result, "total_pages":Total_Pages})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}

@route('/initTimesheet', method=['OPTIONS','GET']) 
def init_sheet():
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    EditExistingSheet = 0
    SheetID = ""
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
            today_sql_format = date.today().strftime('%Y/%m/%d')
            Uid =   verifyToken(Auth)["uid"]
            ExistingTaskSheet=[]
            sql = '''
                        SELECT 
                        id                               
                        FROM sheet   
                        WHERE uid = %s 
                        AND   date = %s       
                  '''
            SheetID = fetch(sql,(Uid,today_sql_format))
            SheetID = toJson(SheetID,["id",]) 
            if len(SheetID) >0 :
               SheetID = SheetID[0]['id']
               EditExistingSheet = 1
               sql = '''
                        SELECT
                            S.id AS sid ,
                            S.date, 
                            U.name AS employee, 
                            T.name AS name, 
                            T.comment, 
                            T.hours, 
                            T.status, 
                            T.pid AS pid,
                            T.id as id
                        FROM 
                        sheet AS S, users AS U, task AS T, projects AS P
                        WHERE
                            S.id = %s
                        AND
                            T.sid = S.id
                        AND
                            P.id = T.pid 
                        AND 
                            U.id = %s 
                                                                           
                '''               
               TaskSheet = fetch(sql,(SheetID,Uid))
               TaskSheet = toJson(TaskSheet,["sid","date","employee","name","comment","hours","status", "pid","id"])              
               ExistingTaskSheet = TaskSheet
            data = {"projects": result, "date":today, "existingTaskSheet": ExistingTaskSheet, "editExistingSheet": EditExistingSheet, "sheetId": SheetID }                        
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
                else:
                    return {"success":"0", "msg":"Sheet already exists for today"}               
            except Exception as E:
                print("****ERROR****\n", E)
                return {"success":"0", "msg":"Process failed, Error occurred at server end"}
                                
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}

@route('/editSheet', method=['OPTIONS','POST'])
def edit_sheet():
    handlingHeaders()
    Auth = request.headers.get("Authorization") 
    if(Auth):
        if(verifyToken(Auth)["verified"]):
            try:
                Date  = request.forms.get('date', "")
                SheetID  = request.forms.get('sid', "")
                Tasks  = request.forms.get('tasks', [])
                Tasks = json.loads(Tasks)
                #Convert Date to MySQL Format#
                d = datetime.datetime.strptime(Date, '%Y-%m-%d')
                d = datetime.date.strftime(d, "%Y/%m/%d")
                Date = str(d)
                sql = '''DELETE FROM task WHERE sid = %s'''
                delete(sql,(str(SheetID),))
                BulkInsertValues=""                
                for task in Tasks:
                    BulkInsertValues = BulkInsertValues+ '("'+task['name']+ '",' +str(SheetID)+ ',' +str(task['pid'])+ ',' +str(task['hours'])+ ',' +str(task['status'])+ ',"' +task['comment']+'."'+ '),'
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

@route('/getTimesheet', method=['OPTIONS','POST'])  
def get_timesheet():
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):        
        if(verifyToken(Auth)["verified"]):
            User_id_condition = ''' '''
            if verifyToken(Auth)["uid"] is not None and verifyToken(Auth)["uid"]>0:
                User_id_condition = " AND S.uid = " +  str(verifyToken(Auth)["uid"])  + " "  
            Sid  = request.forms.get('sid', None)
            sql = '''
                        SELECT 
                            S.date, 
                            U.name AS employee, 
                            T.name AS task, 
                            T.comment, 
                            T.hours, 
                            T.status, 
                            P.name AS project
                        FROM 
                        sheet AS S, users AS U, task AS T, projects AS P
                        WHERE
                            S.uid = U.id
                        AND
                            T.sid = S.id
                        AND
                            P.id = T.pid
                        ''' + User_id_condition +'''
                        AND 
                            S.id = %s
                 '''     
            result = fetch(sql,(Sid,))    
            result = toJson(result,["date","employee","task","comment","hours","status", "project"])             
            return json.dumps({"success":"1", "data":result})
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"} 


@route('/generateReport', method=['OPTIONS','POST'])  
def generate_report():
    handlingHeaders()
    Auth = request.headers.get("Authorization")
    if(Auth):
        if(verifyToken(Auth)["verified"] and verifyToken(Auth)["isAdmin"]):  
            Project  = request.forms.get('project', None)
            User  = request.forms.get('user', None)
            Start_Date  = request.forms.get('start_date', None)
            End_Date = request.forms.get('end_date', None) 
            Filters = ""
            if int(User) > -3:
                Filters = Filters + " AND S.uid = " + str(User)
            if int(Project) > -3:
                Filters = Filters + " AND T.pid = " + str(Project)                        
            if len(End_Date)>0:
                ed = datetime.datetime.strptime(End_Date, '%Y-%m-%d')
                End_Date = datetime.date.strftime(ed, "%Y/%m/%d")
            if len(Start_Date)>0:
                sd = datetime.datetime.strptime(Start_Date, '%Y-%m-%d')
                Start_Date = datetime.date.strftime(sd, "%Y/%m/%d")
            if len(Start_Date)>0 and len(End_Date)>0:
                Filters = Filters + " AND S.date BETWEEN \"" + Start_Date + "\" AND \"" + End_Date+"\""
            sql = '''
                        SELECT
                        S.date AS Date,
                        P.name AS Project,
                        U.name AS Employee,
                        T.name AS Task,
                        T.hours AS Hours
                        FROM
                        sheet AS S, task AS T, users AS U, projects AS P
                        WHERE
                        T.sid = S.id
                        AND
                        S.uid = U.id
                        AND
                        T.pid = P.id
                ''' + Filters + "  ORDER BY S.date, U.id" 
            result = fetch(sql,())    
            result = toJson(result,["Date","Project","Employee","Task","Hours"])                             
            report = get_xlsx(result)
            response.contet_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response.add_header('Content-Disposition', 'attachment; filename="Report.xlsx"')
            return report.getvalue()                
        else:
            return {"success":"0", "msg":"Authorization Failed"}
    else:
        return {"success":"0", "msg":"Authorization Failed"}   

#-------------Helper Functions ----------------#
def verifyToken(token):    
    sql = '''SELECT * FROM sessions WHERE token = %s'''
    result = fetch(sql,(token,))    
    result = toJson(result,["id","uid","token","designation","timestamp"]) 
    if( time.time() - float(result[0]['timestamp'])  > 28800):
        sql = '''DELETE FROM sessions WHERE token = %s'''
        delete(sql,(result[0]['token']))
        return({"verified":False, "isAdmin":False, "uid": None})
    if len(result) > 0 and result[0]['designation'] == "manager":
        return({"verified":True, "isAdmin":True, "uid": result[0]['uid']})
    elif len(result)>0:
        return({"verified":True, "isAdmin":False, "uid": result[0]['uid']})  
    else :
        return({"verified":False, "isAdmin":False, "uid": None})       

def getLoggedInUserName(token):
        sql = '''SELECT u.name as name FROM users as u, sessions as ses WHERE ses.token = %s AND ses.uid = u.id '''
        result = fetch(sql,(token,))    
        result = toJson(result,["name",]) 
        if len(result) > 0:
            return result[0]
        else:
            return " "

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

def get_xlsx(jsonData):
        try:
            if os.path.exists("./reports/DATAFILE.xlsx"):
                os.remove("./reports/DATAFILE.xlsx")
        except Exception as E:
                print("****ERROR****\n", E)                
        file = BytesIO()
        df_json = DataFrame.from_dict(jsonData)
        df_json.index += 1
        writer = ExcelWriter(file, engine='xlsxwriter')
        df_json.to_excel(writer, sheet_name='Report')
        df_json.to_excel('./reports/DATAFILE.xlsx')
        writer.save()
        return file


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

