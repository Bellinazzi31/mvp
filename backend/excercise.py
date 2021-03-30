import mariadb 
from flask import request, Response
import dbcreds 
import json
import secrets


def get():
    program_id = request.args.get("programId")
    conn = None
    cursor = None
    excercises = None 
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM excercise where program_id = ?",[program_id])
        excercises = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if(excercises !=None):
            excercisesList = []
            for excercise in excercises:
                excer = {
                    "excerciseId" : excercise[0],
                    "programId":excercise[4],
                    "title":excercise[1],
                    "description":excercise[2],
                    "period": excercise[3]
                }
                excercisesList.append(excer)
            return Response(json.dumps(excercisesList,default=str),mimetype="application/json",status=200)
        else:
            return Response("Bad request",mimetype="html/text",status=400) 

def post():
    program_id = request.json.get("programId")
    description = request.json.get("description")
    period = request.json.get("period")
    title = request.json.get("title")
    login_token = request.json.get("loginToken")
    conn = None
    cursor = None
    excercise_id =None
    try:
        conn = mariadb.connect(user=dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user INNER JOIN user_session on user.id = user_session.user_id WHERE user.user_role = ? AND user_session.login_token=?",["Coach",login_token])
        coach = cursor.fetchall()
        if len(coach) == 1 : 
            cursor.execute("INSERT INTO excercise (title,description,program_id,period) VALUES (?,?,?,?)",[title,description,program_id,period])
            conn.commit()
            excercise_id = cursor.lastrowid
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if excercise_id !=None : 
            excercise = {
                "excerciseId" : excercise_id,
                "programId" : program_id,
                "title" : title,
                "description":description,
                "period": period

            } 
            return Response(json.dumps(excercise,default=str),mimetype="application/json",status=201)
        else:
            return Response("Bad request",mimetype="html/text",status=400)

def patch():
    excercise_id = request.json.get("excerciseId")
    description = request.json.get("description")
    period = request.json.get("period")
    title = request.json.get("title")
    login_token = request.json.get("loginToken")
    conn = None
    cursor = None
    excercise = None
    affected_rows = None
    try:
        conn = mariadb.connect(user=dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user INNER JOIN user_session on user.id = user_session.user_id WHERE user.user_role = ? AND user_session.login_token=?",["Coach",login_token])
        coach = cursor.fetchall()
        if len(coach) == 1 :
            if description !=None and description !="" :
                cursor.execute("UPDATE excercise SET description = ? where id =?",[description,excercise_id])
            if period !=None and period !="" :
                cursor.execute("UPDATE excercise SET period = ? where id =?",[period,excercise_id]) 
            if title !=None and title !="" :
                cursor.execute("UPDATE excercise SET title = ? where id =?",[title,excercise_id])     
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.execute("SELECT * FROM excercise where id = ? ",[excercise_id])
            excercise = cursor.fetchall()[0]
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if affected_rows ==1 : 
            excercise_details = {
                "excerciseId" : excercise[0],
                "programId":excercise[4],
                "title":excercise[1],
                "description":excercise[2],
                "period": excercise[3]
            } 
            return Response(json.dumps(excercise_details,default=str),mimetype="application/json",status=201)
        else:
            return Response("Bad request",mimetype="html/text",status=400)

def delete():
    excercise_id = request.json.get("excerciseId")
    login_token = request.json.get("loginToken")
    conn = None
    cursor = None
    affected_rows = None
    try:
        conn = mariadb.connect(user=dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user INNER JOIN user_session on user.id = user_session.user_id WHERE user.user_role = ? AND user_session.login_token=?",["Coach",login_token])
        coach = cursor.fetchall()
        if len(coach) == 1 :
            cursor.execute("DELETE FROM excercise where id = ?",[excercise_id])
            conn.commit()
            affected_rows = cursor.rowcount
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if affected_rows ==1 : 
            return Response("Delete success",mimetype="html/text",status=204)
        else:
            return Response("Bad request",mimetype="html/text",status=400)

