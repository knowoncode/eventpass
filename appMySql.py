from flask import Flask,render_template,request,flash,redirect,url_for,session
from encryption import encrypt
from user import User
from validation import empty,checkAlpha,checkDigit
from admin import Admin
from qrModule import qrGenerator 
from sendEmail import Email

app = Flask(__name__)  #object of class Flask
app.secret_key="jkhjkf67y7844huisy7834hhhgh"

userObj = User()  # create object of User class from user module
adminObj=Admin()
emailObj = Email(app)


@app.route("/")       # @ - decorator 
def home():
    return render_template('home.html')

@app.route("/signUp",methods=["GET","POST"])
def signUp():
    if request.method=="GET":
        return render_template('signUp.html')
    else:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        #--------check empty---------------
        dataList = [firstName,lastName,email,password]
        if empty(dataList):
            flash("Field can't be empty!!!")
            return redirect(url_for("signUp"))

        #--------check alphabate -------------------
        dataList = [firstName,lastName]
        if checkAlpha(dataList):
            flash("name must be alphabate!!!")
            return redirect(url_for("signUp"))
        #-------- encryption-----------------------
        password = encrypt(password)
        status = userObj.userInsert(firstName,lastName,email,password)
        if status:
            flash("Email Already Exists!!")
            return redirect(url_for("signUp"))

        flash("Successfully Registered!! Login Now..")
        return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        email=request.form["email"]
        password=request.form["password"]
        #-------check empty------------------
        dataList = [email,password]
        if empty(dataList):
            flash("Field can't be empty!!!")
            return redirect(url_for("login"))

        password=encrypt(password)
        status = userObj.userLogin(email,password)
        if status:
            return redirect(url_for("userDash"))
        else:
            flash("invalid email and password!!!")
            return redirect(url_for("login"))

@app.route("/userDash")
def userDash():
    return render_template("userDashboard.html")

@app.route("/logout")
def logout():
    session.pop('userEmail')
    session.pop('userName')
    flash('successfully logged out!!!')
    return redirect(url_for("login"))

@app.route("/profile",methods=['GET','POST'])
def profile():
    if request.method=='GET':
        data = userObj.userProfile()
        return render_template("profile.html",record=data)
    else:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        #--------check empty---------------
        dataList = [firstName,lastName]
        if empty(dataList):
            flash("Field can't be empty!!!")
            return redirect(url_for("profile"))

        #--------check alphabate -------------------
        dataList = [firstName,lastName]
        if checkAlpha(dataList):
            flash("name must be alphabate!!!")
            return redirect(url_for("profile"))

        userObj.userProfileUpdate(firstName,lastName)
        flash("your profile updated successfully!!!")
        return redirect(url_for("profile"))

@app.route('/deleteAccount')
def deleteAccount():
    userObj.deleteAccount()
    session.pop('userEmail')
    session.pop('userName')
    flash("Your account is deleted successfully!! Hope to see you again!!")
    return redirect(url_for("signUp"))

@app.route("/changePassword",methods=['GET','POST'])
def changePassword():
    if request.method=='GET':
        return render_template("changePassword.html")
    else:
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        dataList = [oldPassword,newPassword]
        if empty(dataList):
            flash("Field can't be empty!!!")
            return redirect(url_for("changePassword"))
        oldPassword = encrypt(oldPassword)
        newPassword = encrypt(newPassword)
        status = userObj.changePassword(oldPassword,newPassword)
        if status:
            session.pop('userEmail')
            session.pop('userName')
            flash("your password is changed successfully..Login Now!!")
            return redirect(url_for("login"))
        else:
            flash("invalid old password!!")
            return redirect(url_for("changePassword"))

@app.route("/userEventSearch",methods=['GET','POST'])
def userEventSearch():
    if request.method=='GET':
        college = userObj.viewCollege()
        return render_template("userEventSearch.html",college=college)
    else:        
        collegeEmail = request.form['collegeEmail']
        record = userObj.searchEvent(collegeEmail)
        return render_template("userViewEvent.html",record=record)

@app.route("/generatePass",methods=['GET','POST'])
def generatePass():
    if request.method=='GET':
        eventID = request.args.get('eventID')
        event = userObj.generatePass(eventID)
        user = userObj.userProfile()
        img = qrGenerator(event,user)
        status = userObj.eventPass(event[0],user[2],img)
        if status:
            flash("Your Pass is already Generated for this event!! Kindly check your mail!!")
            return redirect(url_for('userEventSearch'))
        else:
            path = f"static/generatePass/event{event[0]}/{img}"
            subject = "EventPass: Event Pass Generate"
            email = session['userEmail']
            message = f'''<h3>Hi <strong>User</strong>, 👋</h3> 
                          <p>Your Pass is Generated Successfully!!</p>
                          <hr>
                          <h5 style="color:red;">EventID: {eventID} </h5>
                          <h5 style="color:blue;">Event Name: {event[1]} </h5>
                          <h5 style="color:blue;">Start Date: {event[2]} </h5>
                          <h5 style="color:blue;">End Date: {event[3]} </h5>
                        <hr>'''
            emailObj.compose(subject,email,message,path,app)
            flash("Your Pass is sent to your emailID!!")
            return redirect(url_for('userEventSearch'))


#------------------------------------------------------------
#------------------- admin ----------------------------------
#------------------------------------------------------------
@app.route("/adminSignUp",methods=['GET','POST'])
def adminSignUp():
    if request.method=="GET":
         return render_template("adminSignUp.html")
    else:
        college=request.form["college"]
        email=request.form["email"]
        password=request.form["password"]
        # ------- check empty-----------
        dataList=[college,email,password]
        if empty(dataList):
            flash("Field cannot be empty!!!")
            return redirect(url_for("adminSignUp"))
        
        #----------encryption-----------
        password=encrypt(password)
        status=adminObj.adminInsert(college,email,password)
        if status:
            flash("Email already Exists!!!")
            return redirect(url_for("adminSignUp"))
                
        flash("Successfully Registered.Login Now...")
        return redirect(url_for("adminLogin"))

@app.route("/adminLogin",methods=['GET','POST'])
def adminLogin():
    if request.method=="GET":
         return render_template("adminLogin.html")
    else:
        email=request.form["email"]
        password=request.form["password"]
        # ------- check empty-----------
        dataList=[email,password]
        if empty(dataList):
            flash("Field cannot be empty!!!")
            return redirect(url_for("adminLogin"))
        password=encrypt(password)
        status=adminObj.adminLogin(email,password)
        if status:
            return redirect(url_for("adminDash"))
        else:
            flash("Invalid email or password!!!")
            return redirect(url_for("adminLogin"))
        return password
        
@app.route("/adminDash")
def adminDash():
     return render_template("adminDashboard.html")

@app.route("/adminLogout")
def adminLogout():
    session.pop('adminEmail')
    session.pop('adminCollege')
    flash('successfully logged out!!!')
    return redirect(url_for("adminLogin"))

@app.route("/adminProfile",methods=['GET','POST'])
def adminProfile():
    if request.method=='GET':
        data=adminObj.adProfile()
        return render_template("adminProfile.html",record=data)
    else:
        college=request.form["college"]
        
       
                # ------- check empty-----------
        dataList=[college]
        if empty(dataList):
                flash("Field cannot be empty!!!")
                return redirect(url_for("adminSignUp"))
        
        #-------- check alphabets-------
        dataList=[college]
        if checkAlpha(dataList):
                flash("Name must be alphabet!!")
                return redirect(url_for("adminSignUp"))

        adminObj.adminProfileUpdate(college)
        flash(" Your Profile updated successfully !!!")
        return redirect(url_for("adminProfile"))

@app.route("/addEvent",methods=['GET','POST'])
def addEvent():
    if request.method=='GET':
        return render_template('addEvent.html')
    else:
        eventName = request.form['eventName']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        venue = request.form['venue']
        capacity = request.form['capacity']
        type = request.form['type']

        # ------- check empty-----------
        dataList=[eventName,startDate,endDate,venue,capacity,type]
        if empty(dataList):
            flash("Field cannot be empty!!!")
            return redirect(url_for("addEvent"))

        adminObj.addEvent(eventName,startDate,endDate,venue,capacity,type)
        flash("event submitted successfully!!!")
        return redirect(url_for("addEvent"))

@app.route("/manageEvent")
def manageEvent():
    record = adminObj.manageEvent()
    return render_template("manageEvent.html",record=record)

@app.route("/deleteEvent")
def daleteEvent():
    eventID = request.args.get('eventID')
    adminObj.deleteEvent(eventID)
    flash("Event is deleted successfully!!!")
    return redirect(url_for('manageEvent'))

@app.route("/updateEvent",methods=['GET','POST'])
def updateEvent():
    if request.method=='GET':
        eventID = request.args.get('eventID')
        record = adminObj.viewEvent(eventID)
        return render_template('updateEvent.html',record=record)
    else:
        eventID = request.args.get('eventID')
        eventName = request.form['eventName']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        venue = request.form['venue']
        capacity = request.form['capacity']
        type = request.form['type']

        # ------- check empty-----------
        dataList=[eventName,startDate,endDate,venue,capacity,type]
        if empty(dataList):
            flash("Field cannot be empty!!!")
            return redirect(url_for("updateEvent",eventID=eventID))

        adminObj.updateEvent(eventID,eventName,startDate,endDate,venue,capacity,type)
        flash("event updated successfully!!!")
        return redirect(url_for("updateEvent",eventID=eventID))

@app.route("/viewEvent")
def viewEvent():
    record = adminObj.manageEvent()
    return render_template("viewEvent.html",record=record)

@app.route("/viewUsers")
def viewUsers():
    eventID = request.args.get('eventID')
    record = adminObj.viewUsers(eventID)
    return render_template("viewUsers.html",record=record)

if __name__=='__main__':
    app.run(debug=True)