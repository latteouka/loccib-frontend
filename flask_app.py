from flask import Flask
from flask import render_template
from flask import request

import os

import pymysql
import pymysql.cursors


app = Flask(__name__)






@app.route('/')
def hello():
    return f'Hello, Heroku!'




@app.route("/getname", methods=['GET'])
def getname():
    name = request.args.get('name')
    return render_template('get.html',**locals())


@app.route("/addnew", methods=['GET'])
def addnew():
    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # add text value
        sql = "INSERT INTO `records` (`header`, `user`, `msg`, `cell_lat`, `cell_lon`, `tri_lat`, `tri_lon`, `url`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, ('即時定位測試', 'chun', '訂位成功', '23', '123', '23', '123', 'http://ggfdg.com'))
        cursor.close()
    connection.commit()
    return f'add new test record'
    
@app.route("/show", methods=['GET'])
def show():
    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `records` WHERE `user`=%s"
        cursor.execute(sql, ('chun',))
        results = cursor.fetchall()
        print(result)
        cursor.close()

    
    return render_template('records.html',**locals())


if __name__ == 'main':
    app.run() #啟動伺服器