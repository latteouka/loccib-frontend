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
    # read parameters
    header = request.args.get('header')
    user = request.args.get('user')
    msg = request.args.get('msg')
    cell_lat = request.args.get('cell_lat')
    cell_lon = request.args.get('cell_lon')
    tri_lat = request.args.get('tri_lat')
    tri_lon = request.args.get('tri_lon')
    time = request.args.get('time')
    stat = request.args.get('stat')

    #url_cell = "http://www.google.com.tw/maps/search/"+cell_lat+","+cell_lon
    #url_tri = "http://www.google.com.tw/maps/search/"+tri_lat+","+tri_lon

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # add text value
        sql = "INSERT INTO `records` (`header`, `user`, `msg`, `cell_lat`, `cell_lon`, `tri_lat`, `tri_lon`, `url`, `time`, `stat`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        cursor.execute(sql, (header, user, msg, cell_lat, cell_lon, tri_lat, tri_lon, "0", time, stat))
        
        cursor.close()

    connection.commit()
    return f'add new test record'
    
@app.route("/show", methods=['GET'])
def show():

    user = request.args.get('user')

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `records` WHERE `user`=%s ORDER BY `id` DESC LIMIT 3"
        cursor.execute(sql, (user,))
        results = cursor.fetchall()
        #print(result)
        cursor.close()

    
    return render_template('records.html',**locals())

@app.route("/target", methods=['GET'])
def target():

    target = request.args.get('target')
    user = request.args.get('user')

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `records` WHERE `user`=%s AND `header`=%s ORDER BY `id` DESC"
        cursor.execute(sql, (user,target))
        results = cursor.fetchall()
        #print(result)
        cursor.close()

    
    return render_template('target_records.html',**locals())


if __name__ == 'main':
    app.run() #啟動伺服器