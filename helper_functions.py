import re
from flask import Flask, render_template, json, jsonify, request, redirect, session, abort,url_for, make_response
from flask_login import LoginManager , login_required , UserMixin , login_user

class User(UserMixin):
    def __init__(self , email , password , id , active=True):
        self.id = id
        self.email = email
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.email , key='secret_key')

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.id = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)

        self.users.setdefault(user.email, user)

    def get_user(self, email):
        return self.users.get(email)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def remove_user(self,userID):
        self.users_id_dict.pop(userID)

def getName(registeredUser, cursor):
        cursor.execute('SELECT name FROM users WHERE email="%s"' % (registeredUser.email))
        names=cursor.fetchall() #should only retrieve one value
        names=re.sub(r'[^\w\s]','',str(names))
        name=names[1:]
        print(names)
        return name

def getPrefandGen(userID, cursor):
        #use of prepared statment
        spq = """SELECT orientation FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        pref=cursor.fetchall()
        pref=re.sub(r'[^\w\s]','',str(pref))
        pref=pref[1:]

        spq="""SELECT sex FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        gender=cursor.fetchall()
        gender=re.sub(r'[^\w\s]','',str(gender))
        gender=gender[1:]

        return pref, gender
