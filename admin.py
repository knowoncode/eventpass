'''
admin table : college, email(Primary Key), password

adminSignUp.html
adminLogin.html
adminDashboard.html

'''
from mysql.connector import connect
from flask import session

mysql_host="localhost"  # 127.0.0.1
mysql_port="3306"
mysql_user="root"
mysql_password="root"

class Admin:
    def __init__(self):
       
        # mysql connection
        con=connect(host=mysql_host,port=mysql_port,user=mysql_user,password=mysql_password)
        cur=con.cursor()
        sq="create database if not exists eventpass"
        cur.execute(sq)
        con.close

    def connection(self):
        con=connect(host=mysql_host,port=mysql_port,user=mysql_user,password=mysql_password,database="eventpass")
        return con
    
    def adminInsert(self,college,email,password):
        db=self.connection()
        cur=db.cursor()
        sq=''' create table if not exists admin(
               college varchar(255),
               email varchar(255),
               password varchar(255),
               primary key(email)
            )'''
        cur.execute(sq)
        #-----insertion---
        #----- Check duplicate------
        cur.execute("select 1 from admin where email=%s",(email,))
        exist=cur.fetchone()
        if exist:
            db.close()
            return 1
        
        sq="insert into admin(college,email,password) values(%s,%s,%s)"
        record=[college,email,password]
        cur.execute(sq,record)
        db.commit() # to save data permanently in database
        db.close()
        return 0
    
    def adminLogin(self,email,password):
        db=self.connection()
        cur=db.cursor()
        sq="select college,email from admin where email=%s and password=%s"
        value=[email,password]
        cur.execute(sq,value)
        row=cur.fetchall()
        db.close()
        if row:
            session["adminCollege"]=row[0][0]
            session["adminEmail"]=row[0][1]
            return True
        else:
            return False

    def adProfile(self):
            db=self.connection()
            cur=db.cursor()
            sq="select college,email from admin where email=%s"
            value=[session['adminEmail']]
            cur.execute(sq,value)
            row=cur.fetchall()
            db.close()
            return row 

    def adminProfileUpdate(self,college):
            db=self.connection()
            cur=db.cursor()
            sq= "update admin set college=%s where email=%s"
            value=[college,session['adminEmail']]
            cur.execute(sq,value)
            db.commit()
            session['adminCollege']=college
            db.close()

    def addEvent(self,eventName,startDate,endDate,venue,capacity,type):
        db=self.connection()
        cur=db.cursor()
        sq=''' create table if not exists event(
               eventID int AUTO_INCREMENT,
               adminEmail varchar(255),
               eventName varchar(255),
               startDate date,
               endDate date,
               venue varchar(255),
               capacity int,
               type varchar(255),
               primary key(eventID)
            )AUTO_INCREMENT=101;'''
        cur.execute(sq)

        sq="insert into event(adminEmail,eventName,startDate,endDate,venue,capacity,type) values(%s,%s,%s,%s,%s,%s,%s)"
        record=[session['adminEmail'],eventName,startDate,endDate,venue,capacity,type]
        cur.execute(sq,record)
        db.commit() # to save data permanently in database
        db.close()
        db.close()

    def manageEvent(self):
        db=self.connection()
        cur=db.cursor()
        sq="select eventID,eventName,startDate,endDate,venue,capacity,type from event where adminEmail=%s"
        value=[session['adminEmail']]
        cur.execute(sq,value)
        row=cur.fetchall()
        db.close()
        return row 

    def deleteEvent(self,eventID):
        db=self.connection()
        cur=db.cursor()
        sq = "delete from event where eventID=%s"
        record = [eventID]
        cur.execute(sq,record)
        db.commit()
        db.close()

    def viewEvent(self,eventID):
        db=self.connection()
        cur=db.cursor()
        sq="select eventID,eventName,startDate,endDate,venue,capacity,type from event where eventID=%s"
        value=[eventID]
        cur.execute(sq,value)
        row=cur.fetchall()
        db.close()
        return row 

    def updateEvent(self,eventID,eventName,startDate,endDate,venue,capacity,type):
        db=self.connection()
        cur=db.cursor()
        sq = "update event set eventName=%s,startDate=%s,endDate=%s,venue=%s,capacity=%s,type=%s  where eventID=%s"
        record = [eventName,startDate,endDate,venue,capacity,type,eventID]
        cur.execute(sq,record)
        db.commit()
        db.close()

    def viewUsers(self,eventID):
        db=self.connection()
        cur=db.cursor()
        sq="select eventID,firstName,lastName from eventpass e join users u on e.email=u.email where eventID=%s"
        value=[eventID]
        cur.execute(sq,value)
        row=cur.fetchall()
        db.close()
        return row 

    def passCount(self,eventID):
        db=self.connection()
        cur=db.cursor()
        sq="select count(eventID) from eventpass where eventID=%s"
        value=[eventID]
        cur.execute(sq,value)
        row=cur.fetchall()
        db.close()
        return row 


