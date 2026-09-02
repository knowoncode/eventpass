from flask_mail import *

class Email:
    def __init__(self,app):
        #-------------------mail configuration---------------------------
        app.config["MAIL_SERVER"]='smtp.gmail.com'
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USERNAME"] = 'knowon.edu@gmail.com'
        app.config["MAIL_PASSWORD"]= 'swik mzrz xmpe ebkd'
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USE_SSL"] = False
        app.config["MAIL_TIMEOUT"] = 20
        self.mail = Mail(app)  #Mail class object create

    def compose(self,subject,email,message,path,app):
        msg = Message(subject,sender=app.config["MAIL_USERNAME"],recipients=[email])
        msg.html = message
        # Open and read the image binary file
        with app.open_resource(path) as fp:
            msg.attach(
                filename="qrPassImage.png",       # Name visible to the recipient
                content_type="image/png",   # MIME type of the file
                data=fp.read()              # File contents
            )
        self.mail.send(msg)