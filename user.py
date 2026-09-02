from mysql.connector import connect
from flask import session

mysql_host = "localhost"  #127.0.0.1
mysql_port = "3306"
mysql_user = "root"
mysql_password = "root"

class User:
    def __init__(self):
        #mysql connection
        con = connect(host=mysql_host,port=mysql_port,user=mysql_user,password=mysql_password)
        cur = con.cursor()
        sq = "create database if not exists eventpass"
        cur.execute(sq)
        con.close()

    def connection(self):
        con = connect(host=mysql_host,port=mysql_port,user=mysql_user,password=mysql_password,database="eventpass")
        return con

    def userInsert(self,firstName,lastName,email,password):
        db = self.connection()
        cur = db.cursor()
        sq = '''create table if not exists users(
                firstName varchar(255),
                lastName varchar(255),
                email varchar(255),
                password varchar(255),
                primary key(email)
                )'''
        cur.execute(sq)
        #----------------------insertion-------------------
        #check duplicate
        cur.execute("select 1 from users where email=%s",(email,))
        exist = cur.fetchone()
        if exist:
            db.close()
            return 1

        sq = "insert into users(firstName,lastName,email,password)values(%s,%s,%s,%s)"
        record = [firstName,lastName,email,password]
        cur.execute(sq,record)
        db.commit()  # to save data permanently in db
        db.close()
        return 0

    def userLogin(self,email,password):
        db = self.connection()
        cur = db.cursor()
        sq = "select firstName,email from users where email=%s and password=%s"
        value=[email,password]
        cur.execute(sq,value)
        row = cur.fetchall()
        db.close()
        if row:
            session['userName'] = row[0][0]
            session['userEmail'] = row[0][1]
            return True
        else:
            return False

    def userProfile(self):
        db = self.connection()
        cur = db.cursor()
        sq = "select firstName,lastName,email from users where email=%s"
        value=[session['userEmail']]
        cur.execute(sq,value)
        row = cur.fetchone()
        db.close()
        return row

    def userProfileUpdate(self,firstName,lastName):
        db = self.connection()
        cur = db.cursor()
        sq = "update users set firstName=%s,lastName=%s where email=%s"
        value=[firstName,lastName,session['userEmail']]
        cur.execute(sq,value)
        db.commit()
        session['userName'] = firstName
        db.close()

    def deleteAccount(self):
        db = self.connection()
        cur = db.cursor()
        sq = "delete from users where email=%s"
        value=[session['userEmail']]
        cur.execute(sq,value)
        db.commit()
        db.close()

    def changePassword(self,oldPassword,newPassword):
        db = self.connection()
        cur = db.cursor()
        sq = "select 1 from users where email=%s and password=%s"
        value=[session['userEmail'],oldPassword]
        cur.execute(sq,value)
        row = cur.fetchall()
        if row:
            sq = "update users set password=%s where email=%s"
            value=[newPassword,session['userEmail']]
            cur.execute(sq,value)
            db.commit()
            db.close()
            return True
        else:
            db.close()
            return False

    def viewCollege(self):
        db = self.connection()
        cur = db.cursor()
        sq = "select college,email from admin"
        cur.execute(sq)
        row = cur.fetchall()
        return row

    def searchEvent(self,collegeEmail):
        db = self.connection()
        cur = db.cursor()
        sq = "select eventID,eventName,startDate,endDate,venue,capacity,type from event where adminEmail=%s and endDate >= curdate()"
        value=[collegeEmail]
        cur.execute(sq,value)
        row = cur.fetchall()
        return row

    def generatePass(self,eventID):
        db = self.connection()
        cur = db.cursor()
        sq = "select eventID,eventName,startDate,endDate,type from event where eventID=%s"
        value=[eventID]
        cur.execute(sq,value)
        row = cur.fetchone()
        return row

    def eventPass(self,eventID,email,img):
        db = self.connection()
        cur = db.cursor()
        sq = '''create table if not exists eventPass(
                eventID int,
                email varchar(255),
                img varchar(255),
                primary key(eventID,email)
                )'''
        cur.execute(sq)
        #----------------------insertion-------------------
        #check duplicate
        cur.execute("select 1 from eventPass where email=%s and eventID=%s",(email,eventID))
        exist = cur.fetchone()
        if exist:
            db.close()
            return True

        sq = "insert into eventPass(eventID,email,img)values(%s,%s,%s)"
        record = [eventID,email,img]
        cur.execute(sq,record)
        db.commit()  
        db.close()
        return 0