#pip install pyqrcode
#pip install pypng
import pyqrcode
import os


def qrGenerator(event,user):
    value=f'''EventID:{event[0]},
              Event Name:{event[1]},
              Start Date:{event[2]},
              End Date:{event[3]},
              Type:{event[4]},
              Name : {user[0]} {user[1]}
              '''
    qr = pyqrcode.create(value)
    img = f"{user[2]}.png"
    os.makedirs(f"static/generatePass/event{event[0]}",exist_ok=True)
    qr.png(f"static/generatePass/event{event[0]}/{img}",scale=3)
    return img


if __name__=="__main__":
    qrGenerator()