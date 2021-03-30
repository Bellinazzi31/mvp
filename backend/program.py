import mariadb 
from flask import request, Response
import dbcreds 
import json
import secrets


def get():
    user_id = request.args.get("traineeId")
    conn = None
    cursor = None
    programs = None 
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM program where trainee_id = ?",[user_id])
        programs = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if(programs !=None):
            programList = []
            for program in programs:
                prog = {
                    "programId" : program[0],
                    "description":program[1],
                    "traineeId":program[2],
                    "period": program[3]
                }
                programList.append(prog)
            return Response(json.dumps(programList,default=str),mimetype="application/json",status=200)
        else:
            return Response("Bad request",mimetype="html/text",status=400) 

def post():
    trainee_id = request.json.get("traineeId")
    description = request.json.get("description")
    period = request.json.get("period")
    login_token = request.json.get("loginToken")
    conn = None
    cursor = None
    program_id =None
    try:
        conn = mariadb.connect(user=dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user INNER JOIN user_session on user.id = user_session.user_id WHERE user.user_role = ? AND user_session.login_token=?",["Coach",login_token])
        coach = cursor.fetchall()
        if len(coach) == 1 : 
            cursor.execute("INSERT INTO program (description,trainee_id,period) VALUES (?,?,?)",[description,trainee_id,period])
            conn.commit()
            program_id = cursor.lastrowid
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if program_id !=None : 
            program = {
                "programId" : program_id,
                "description":description,
                "traineeId":trainee_id,
                "period": period

            } 
            return Response(json.dumps(program,default=str),mimetype="application/json",status=201)
        else:
            return Response("Bad request",mimetype="html/text",status=400)

def patch():
    program_id = request.json.get("programId")
    description = request.json.get("description")
    period = request.json.get("period")
    login_token = request.json.get("loginToken")
    conn = None
    cursor = None
    program = None
    affected_rows = None
    try:
        conn = mariadb.connect(user=dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password,database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user INNER JOIN user_session on user.id = user_session.user_id WHERE user.user_role = ? AND user_session.login_token=?",["Coach",login_token])
        coach = cursor.fetchall()
        if len(coach) == 1 :
            if description !=None and description !="" :
                cursor.execute("UPDATE program SET description = ? where id =?",[description,program_id])
            if period !=None and period !="" :
                cursor.execute("UPDATE program SET period = ? where id =?",[period,program_id]) 
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.execute("SELECT * FRoM program where id = ? ",[program_id])
            program = cursor.fetchall()[0]
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close
        if affected_rows ==1 : 
            program_details = {
                "programId" : program[0],
                "description": program[1],
                "traineeId": program[2],
                "period": program[3]

            } 
            return Response(json.dumps(program,default=str),mimetype="application/json",status=201)
        else:
            return Response("Bad request",mimetype="html/text",status=400)

def delete():
    program_id = request.json.get("programId")

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
            cursor.execute("DELETE FROM program where id = ?",[program_id])
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

