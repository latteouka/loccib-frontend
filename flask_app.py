from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import url_for
from flask import redirect
from flask import flash

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import os

import pymysql
import pymysql.cursors

import csv
import io


app = Flask(__name__)
app.secret_key = '268ffece5b07530333f1695850c5febd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請登入！！'

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(使用者):
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者
    return user

@login_manager.request_loader
def request_loader(request):
    使用者 = request.form.get('user_id')
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[使用者]['password']

    return user

users = {'chun': {'password': 'L26311615'},}




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
@login_required
def show():

    user = request.args.get('user')

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `records` WHERE `user`=%s ORDER BY `id` DESC LIMIT 100"
        cursor.execute(sql, (user,))
        results = cursor.fetchall()
        #print(result)
        cursor.close()

    
    return render_template('records.html',**locals())

@app.route("/target", methods=['GET'])
@login_required
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
        
        cursor.close()

    
    return render_template('target_records.html',**locals())


@app.route('/export', methods=['GET'])
def export():

    target = request.args.get('target')
    user = request.args.get('user')

    si = io.StringIO()
    cw = csv.writer(si)

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
        
        cursor.close()

    cw.writerow((['Target', 'Time', 'Cell', 'Tri_Loc', 'Info']))
    
    for result in results:
        cw.writerow(([result["header"],result["time"],"http://www.google.com.tw/maps/search/"+result["cell_lat"]+","+result["cell_lon"],"http://www.google.com.tw/maps/search/"+result["tri_lat"]+","+result["tri_lon"],result["msg"]]))

    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=output.csv'
    response.headers["Content-type"] = "text/csv"
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    使用者 = request.form['user_id']
    if (使用者 in users) and (request.form['password'] == users[使用者]['password']):
        user = User()
        user.id = 使用者
        login_user(user)
        flash(f'Hi, {使用者}！')
        return redirect(url_for('show'))

    flash('登入失敗了...')
    return render_template('login.html')

@app.route('/logout')
def logout():
    使用者 = current_user.get_id()
    logout_user()
    flash(f'{使用者}！掰掰！')
    return render_template('login.html')


if __name__ == 'main':
    app.run() #啟動伺服器