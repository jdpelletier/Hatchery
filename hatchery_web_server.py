import os
import datetime

from flask import Flask, redirect, request, url_for
from home import home

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def home_():
    parent_directory = "C:/Users/johnp/Desktop/Kohanakai/Hatchery/TestData"
    ## for testing button, erase later
    today = datetime.date.today()
    # yesterday = today - datetime.timedelta(days=9)
    ##
    # currentDay = datetime.date.today()
    todaystr = today.isoformat()
    path = os.path.join(parent_directory, todaystr)
    filepath = os.path.join(str(path), "dataFile.txt")
    return home(filepath)

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 50009
    app.run(host=host,port=port)
