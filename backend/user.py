import mariadb
from flask import request, Response
import dbcreds
import json
import secrets

def get():
    token = request.args.get("loginToken")
    user_id = request.args.get("userId")
    # user id 2 is used to identify the id of the logged in user that is asking for the info
    users = None
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.username, port = dbcreds.port, host = dbcreds.host, password = dbcreds.password, database = dbcreds.database)
        cursor = conn.cursor()
        if token !=None :
            cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
            user_id_2 = str(cursor.fetchone()[0])
        if user_id_2 != None:
            if user_id_2 == user_id:
                cursor.execute("SELECT * FROM user where id =?",[user_id])
            else:
                cursor.execute("SELECT * FROM user where id = ? and user_role = 'Coach' ",[user_id_2]) 
                user = cursor.fetchall()
                if len(user) == 1:
                    if user_id !=None:
                        cursor.execute("SELECT * FROM user where id =?",[user_id])
                    else:
                        cursor.execute("SELECT * FROM user")   
            users = cursor.fetchall()
    except Exception as e :
        print(e)
    finally:
        if(conn != None):
            conn.close()
        if (cursor !=None):
            cursor.close
        if users !=None or users == []:
            listofusers = []
            for user in users:
                dic = {
                    "userId": user[0],
                    "name": user[1],
                    "username": user[2],
                    "email": user[4],
                    "birthdate": user[5],
                    "weight": user[6],
                    "height": user[7],
                    "role": user[8]
                }                  
                listofusers.append(dic)
            return Response(json.dumps(listofusers,default=str),mimetype="application/json",status=200)
        else:
            return Response("bad request",mimetype="html/text",status=400)    

def post():
    name = request.json.get("name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    birthday = request.json.get("birthday")
    weight = request.json.get("weight")
    height = request.json.get("height")
    rows = None

    try: 
        conn = mariadb.connect(user=dbcreds.username, port = dbcreds.port, host = dbcreds.host, password = dbcreds.password, database = dbcreds.database)
        cursor = conn.cursor()
        if name != None and username != None and email != None and password !=None and birthday !=None and weight !=None and height != None:
            cursor.execute("INSERT INTO user (name,username,email,password,birthday,weight,height) VALUES (?,?,?,?,?,?,?)",[name,username,email,password,birthday,weight,height])
            conn.commit()
            rows = cursor.rowcount


    except Exception as ex:
        print(ex)

    finally: 
        if(conn != None):
            conn.close()
        if (cursor !=None):
            cursor.close
        if (rows == 1):
            return Response("success",mimetype="html/text",status=201)
        else:
            return Response("failure",mimetype="html/text",status=400) 

def patch():
    token = request.json.get("loginToken")
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    name = request.json.get("name")
    birthday = request.json.get("birthday")
    height = request.json.get("height")
    weight = request.json.get("weight")
    affected_rows = None
    userId = None
    user = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_session WHERE login_token = ?", [token])
        userId = cursor.fetchall()[0][0]
        if username != None :
            cursor.execute("UPDATE user SET username = ? Where id = ?",[username,userId])
        if email != None :
            cursor.execute("UPDATE user SET email = ? where id = ?",[email,userId])
        if password != None :
            cursor.execute("UPDATE user SET password = ? where id = ?",[password,userId])
        if name != None :
            cursor.execute("UPDATE user SET name = ? where id = ?",[name,userId]) 
        if birthday != None :
            cursor.execute("UPDATE user SET birthday = ? where id = ?",[birthday,userId]) 
        if height != None :
            cursor.execute("UPDATE user SET height = ? where id = ?",[height,userId]) 
        if weight != None :
            cursor.execute("UPDATE user SET weight = ? where id = ?",[weight,userId])                   
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.execute("SELECT * from user WHERE id =?",[userId])
        user = cursor.fetchall()[0]
    except Exception as ex :
        print("exception is :" + ex )  
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if affected_rows == 1:
            user_dic = {
                "userId": user[0],
                "name": user[1],
                "email": user[4],
                "username": user[2],
                "height": user[7],
                "weight": user[6],
                "birthday": user[5]
            }
            return Response (json.dumps(user_dic,default=str),mimetype="application/json",status=200)
        else:
            return Response("user patch failed",mimetype="html/text",status=400) 
                                      
def delete():
    token = request.json.get("loginToken")
    password = request.json.get("password")
    affected_rows = None
    
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host =dbcreds.host , password = dbcreds.password , database= dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_session WHERE login_token = ?",[token])
        userId = cursor.fetchall()[0][0]
        cursor.execute("SELECT password FROM user where id = ?" , [userId])
        user_password = cursor.fetchall()[0][0]
        if(password == user_password):
            cursor.execute("DELETE FROM user where id = ?",[userId])
            conn.commit()
            affected_rows = cursor.rowcount
    except Exception as ex : 
        print("exception is :" + ex )
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if affected_rows == 1: 
            return Response ("user delete success",mimetype="html/text",status=204)
        else:
            return Response("user delete failed",mimetype="html/text",status=400)                                      
                    
        