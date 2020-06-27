import os
import datetime

from flask import Flask
from home import home

app = Flask(__name__)

# Establish etcgui route

@app.route('/')
def home_():
    parent_directory = "/home/pi/Desktop/Hatchery/TestData"
    currentDay = datetime.date.today()
    todaystr = currentDay.isoformat()
    path = os.path.join(parent_directory, todaystr)
    filepath = os.path.join(str(path), "dataFile.txt")
    return home(filepath)

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 50009
    app.run(host=host,port=port)