from bottle import route, run, post, get, request, static_file, template, response
from query import fetch, update, insert, delete
import collections
import requests
import json
import random
import binascii


@route('/', method='GET')
def login():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    return template('./index')

@route('/home', method='GET')
def home():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    return template('./app')

### API SECTION ###
@route('/login', method='POST')
def login_api():   
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Account  = request.forms.get('user_id', None)
    Password = request.forms.get('user_pwd', None)
    Password = Password.encode('ascii')
    Password = bin(int(binascii.hexlify(Password),16))    
    sql = '''SELECT * FROM credentials WHERE account = ? AND password = ? ''' 
    result = fetch(sql,[Account,Password,]) 
    Token = None   
    if len(result)>0:
        Token = random.randint(1120501,5300080)
        sql = '''UPDATE credentials SET token = ? WHERE account = ?'''
        update(sql,[Token,Account]) 
        return {"success":"1", "token":Token}
    else:
        return {"success":"0", "token":Token}        


@route('/getAccountType', method='POST')
def login_api():   
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}    
    sql = '''SELECT type FROM credentials WHERE token = ? ''' 
    result = fetch(sql,[Token]) 
    result = toJson(result,["type"])   
    return json.dumps({"success":"1", "data":result})  


@route('/getUsers', method='POST')
def user_list():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Sort  = request.forms.get('sort', None)
    sql = '''SELECT * from investors ORDER BY ?'''
    result = (fetch(sql,[Sort,]))
    result = toJson(result,["name","id","status"])    
    return json.dumps({"success":"1", "data":result})

@route('/saveUser', method='POST')
def user_list():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Id  = request.forms.get('id', None)
    Name  = request.forms.get('name', None)
    Status  = request.forms.get('status', None)
    sql = '''SELECT * from investors WHERE id = ?'''
    result = (fetch(sql,[Id,]))
    if len(result) > 0: 
        sql = '''UPDATE investors SET name = ?, status = ? WHERE id = ?'''
        update(sql,[Name,Status,Id])
    else:
        sql=''' INSERT INTO investors(name,status) VALUES (?,?)'''
        insert(sql,[Name,Status,])
    return json.dumps({"success":"1", "data":result})


@route('/getItems', method='POST')
def item_list():    
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    Search = request.forms.get('search', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Sort  = request.forms.get('sort', None)  
    sql = "SELECT * from items" 
    if Search:
             sql = sql+" where name like '%"+Search+"%'"   
    sql = sql+" order by name"           
    result = (fetch(sql,[]))       
    result = toJson(result,
    [   "id",
        "name",
        "price",
        "unit",      
    ])        
    return json.dumps({"success":"1", "data":result})

@route('/newItem', method='POST')
def insert_item():    
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)    
    Name  = request.forms.get('name', None)
    Price  = request.forms.get('price', None)
    Unit  = request.forms.get('unit', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}    
    sql = '''INSERT INTO items (name, price, unit) VALUES (?,?,?)''' 
    insert(sql,[Name,Price,Unit,])             
    return json.dumps({"success":"1"})


@route('/deleteItem', method='POST')
def delete_item():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Id = request.forms.get('id', None)      
    sql = "DELETE FROM items WHERE id= " + Id;
    delete(sql,[])
    return json.dumps({"success":"1"})


@route('/getItem', method='POST')
def get_item():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)    
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Id = request.forms.get('id', None)      
    sql = "SELECT * FROM items WHERE id= ?" ;
    result = (fetch(sql,[Id,]))    
    result = toJson(result,
    [   "id",
        "name",
        "price",
        "unit",      
    ])  
    return json.dumps({"success":"1", "data":result})

@route('/editItem', method='POST')
def save_item():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Id = request.forms.get('id', None)
    Name = request.forms.get('name', None)  
    Price = request.forms.get('price', None)  
    Unit = request.forms.get('unit', None)     
    sql='''UPDATE items SET 
    name=?,price=?,unit=?
    WHERE id = ?'''
    update(sql,[Name,Price,Unit,Id])    
    return {"success":"1"}

@route('/getItemsSelect', method='POST')
def get_item():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)    
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Id = request.forms.get('id', None)      
    sql = "SELECT name as label, id as value, price, unit FROM items" ;
    result = (fetch(sql,[]))    
    result = toJson(result,
    [   "label",
        "value",
        "price",
        "unit",      
    ])  
    return json.dumps({"success":"1", "data":result})

@route('/saveOrderInvoice', method='POST')
def insert_item():    
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)        
    Price  = request.forms.get('price', None)
    Date  = request.forms.get('date', None)
    Paid  = request.forms.get('paid', None)
    Discount  = request.forms.get('discount', None)
    Net  = request.forms.get('net', None)
    Items = request.forms.get('items', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}    
    sql = '''INSERT INTO invoices (date, price, paid, net, discount, items) VALUES (?,?,?,?,?,?)''' 
    insert(sql,[Date,Price,Paid,Net,Discount,Items])             
    return json.dumps({"success":"1"})


@route('/getInvoices', method='POST')
def initial_data():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    ToDate = request.forms.get('to_date', None) 
    FromDate = request.forms.get('from_date', None)  
    sql = '''SELECT * FROM invoices WHERE date BETWEEN '''
    sql = sql+"'"+FromDate+"'" 
    sql = sql+" AND '"+ToDate+"'" 
    sql = sql+" ORDER BY id DESC"     
    result = (fetch(sql,[]))    
    result = toJson(result,
    [   "id",
        "date",
        "price",
        "paid",
        "discount",
        "items",  
        "net"
    ])  
    return json.dumps({"success":"1", "data":result})
   
@route('/deleteInvoice', method='POST')
def delete_item():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)
    if verifyToken(Token) == 0 :
        return {"success":"0", "msg":"Authentication Failed!"}
    Id = request.forms.get('id', None)      
    sql = "DELETE FROM invoices WHERE id= " + Id;
    delete(sql,[])
    return json.dumps({"success":"1"})

@route('/logout', method='POST')
def kill_session():
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET, POST")
    Token  = request.forms.get('token', None)              
    sql = "UPDATE credentials SET token = null";
    update(sql,[])
    return json.dumps({"success":"1"})



#-------------Helper Functions ----------------#
def verifyToken(token):
    sql = '''SELECT * FROM credentials WHERE token = ?'''
    result = fetch(sql,[token,]) 
    return(len(result))

def toJson(result,keys):
    objects_list = []
    for row in result: 
        d = {}
        for index,item in enumerate (row, start=0):                                    
            d[keys[index]] = item      
        objects_list.append(d)
    return (objects_list)


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
