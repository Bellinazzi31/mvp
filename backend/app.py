from flask import Flask, request, Response
import mariadb
import dbcreds
import user
import program
import excercise
import login

from flask_cors import CORS 
app = Flask(__name__)
CORS(app)

@app.route("/api/users", methods = ["GET", "POST", "PATCH", "DELETE"])
def users():
    if request.method == "GET":
        return user.get()
    elif request.method == "POST":
        return user.post()
    elif request.method == "PATCH":
        return user.patch()
    elif request.method == "DELETE":
        return user.delete()
    else :
        Response("Not Supported", mimetype="text/html",status=500)    
@app.route("/api/login", methods = ["POST", "DELETE"])
def user_login():
    if request.method == "POST":
        return login.post()
    elif request.method == "DELETE":
        return login.delete()
    else :
        Response("Not Supported", mimetype="text/html",status=500) 
@app.route("/api/program", methods = ["GET", "POST", "PATCH", "DELETE"])        
def user_program():
    if request.method == "GET":
        return program.get()
    elif request.method == "POST":
        return program.post()
    elif request.method == "PATCH":
        return program.patch()
    elif request.method == "DELETE":
        return program.delete()
    else :
        Response("Not Supported", mimetype="text/html",status=500) 
@app.route("/api/excercise", methods = ["GET", "POST", "PATCH", "DELETE"])         
def user_excercise():
    if request.method == "GET":
        return excercise.get()
    elif request.method == "POST":
        return excercise.post()
    elif request.method == "PATCH":
        return excercise.patch()
    elif request.method == "DELETE":
        return excercise.delete()
    else :
        Response("Not Supported", mimetype="text/html",status=500)          
               
