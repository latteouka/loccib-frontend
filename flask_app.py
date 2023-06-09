from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import Response
from flask import url_for
from flask import redirect
from flask import flash
from flask import session

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import os

import pymysql
import pymysql.cursors

import csv
import io
from io import BytesIO, TextIOWrapper

from datetime import datetime,timezone,timedelta
from datetime import date
import datetime

import hashlib

import re
from ipwhois import IPWhois
from pprint import pprint

import secrets
import pyshorteners



app = Flask(__name__)
app.secret_key = '268ffece5b07530333f1695850c5febd'

#app.debug = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請登入！！'


def which_isp(ip):

    is_twm = False

    if '49.214.' in ip:
        is_twm = True
    elif '49.215.' in ip:
        is_twm = True
    elif '49.216.' in ip:
        is_twm = True
    elif '49.217.' in ip:
        is_twm = True
    elif '49.218.' in ip:
        is_twm = True
    elif '49.219.' in ip:
        is_twm = True
    elif '175.96.' in ip:
        is_twm = True
    else:
        is_twm = False
    

    results = IPWhois(ip).lookup_rdap(asn_methods=['dns', 'whois', 'http'])
  

    if is_twm:
        return '台灣大哥大', '使用者資料'
    elif results['network']['name'] == 'HINET-NET':
        return '中華電信網路', '使用者資料'
    elif results['network']['name'] == 'EMOME-NET':
        return '中華電信行動', '使用者資料'
    elif results['network']['name'] == 'taiwanmobile-net':
        return '台灣大哥大', '使用者資料'
    elif results['network']['name'] == 'TAIWANMOBILE-NET':
        return '台灣大哥大', '使用者資料'
    elif results['network']['name'] == 'FETNET-NET':
        return '遠傳電信股份有限公司', '使用者資料'
    elif results['network']['name'] == 'FEG-MPLS-NETWORK-NET':
        return '遠傳電信股份有限公司', '使用者資料'
    elif results['network']['name'] == 'VIBO-NET':
        return '台灣之星', '使用者資料'
    elif results['network']['name'] == 'VEETIME-TW':
        return '大台中數位有線電視股份有限公司', '歷史查詢'
    elif results['network']['name'] == 'APT':
        return '亞太電信', '歷史查詢'
    elif results['network']['name'] == 'APOL-NET':
        return '亞太電信', '歷史查詢'
    elif results['network']['name'] == 'TFN-NET':
        return '台灣固網', '歷史查詢'
    elif results['network']['name'] == 'NCICNET-NET':
        return '新世紀資通請發文', '使用者資料'
    else:
        return '不能投單的業者', '使用者資料'

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

    #hash
    s = hashlib.sha1()
    request_password = request.form['password'].encode('utf-8')
    s.update(request_password)
    request_password_h = s.hexdigest()

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    #user.is_authenticated = request.form['password'] == users[使用者]['password']
    user.is_authenticated = request_password_h == users[使用者]['password']

    return user

users = {'chun': {'password': '70608f1675a12b81a09aa5f797b5b5d308b5405d'},
        'loveve': {'password': 'e315ceef29e03c0360070a952eba732306ba3f7c'},
        'loveve3': {'password': 'e315ceef29e03c0360070a952eba732306ba3f7c'},
        'loveve2': {'password': '0f86d97a93185f41c034e6abae1ef82af85a638c'},
        'pa781022': {'password': '3a960464d36c1b8bad183ed57ee79c0e39953cce'},
        'ci771047': {'password': '3a960464d36c1b8bad183ed57ee79c0e39953cce'},
        'lawbingbing': {'password': 'a57ae0fe47084bc8a05f69f3f8083896f8b437b0'},
        'p689688': {'password': 'a57ae0fe47084bc8a05f69f3f8083896f8b437b0'},
        'p689690': {'password': '4e0c1441681c0d6101c1c667a98eca93705f6bed'},
        'p689691': {'password': '46cd50d19a96e8c2d61b5218f9fd163be9e73420'},
        'p689692': {'password': '8631d03874b1859adbb0479ce23db9fba949c541'},
        'fishcan': {'password': 'xxx'},
        'yifan': {'password': '0e19644e35a2b71ff35115c2d7a68a65fd76ce7e'},
        'icad001': {'password': 'c875c8c4266da482b8b0470107d8f09f60abe6c3'},
        'icad002': {'password': '5b0d403f091ba39ce0f9e3760007d94261678184'},
        'icad003': {'password': '212c57b53dfb7b03870137d82c95370fa2eb19eb'},
        'icad004': {'password': 'b6e4f86080f14e6ecffad598a43f9e8cbaf3ff22'},
        'icad005': {'password': '6544987510e73c367bd53fa5aa0277ee8072c85f'},
        'icad006': {'password': 'acd45bc79ee546c7f577c6a6504bbd8173ea7eb3'},
        'mpfive77': {'password': '9977aa0f876371d2957cb5a7949122f6a55a8d02'},
        'cibdodo': {'password': '8b029d563ed25f7224dedf1b0d5290bb11d8ae84'},
        'cibpopo': {'password': '0c663143b30be921fdbd51d53f394976d5f1059f'},
        'yty': {'password': '507e2ae9ac0ff334fab81b6c4bed301ceac96d94'},
        'Ss07': {'password': 'a15407ea17c685de00cdf080c7078bd42c944d3a'},
        'Ss08': {'password': '67af763ba74c29da61639d6d9e98860e8e0607d5'},
        'linantaj': {'password': '1fd0cd0b10b84e9afa697908f04135295977e2d5'},
        'bigcat': {'password': '06304e3f440af4dd29ae2822028ffc51445cc4ab'},
        'markhong': {'password': '0ddb5877c896f43e8734e10b001e7f1eb92889cd'},
        'bicel20306': {'password': 'dca58304a8394ac4181d0134189f6e6916914212'},
        'system001': {'password': '0f86d97a93185f41c034e6abae1ef82af85a638c'},
        'cjd98xtd': {'password': '7c4a8d09ca3762af61e59520943dc26494f8941b'},
        'dohoa61420': {'password': '39dcef89803730670d34064bd95d49330c1e6ff8'},
        'R223571705': {'password': '3655bf2b31a3016299b8d9e2c79754f99eadabda'}
}


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
    connection.close()
    return f'add new record'
    
@app.route("/", methods=['GET'])
@login_required
def show():

    user = current_user.get_id()

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `records` WHERE `user`=%s ORDER BY `id` DESC LIMIT 2000"
        cursor.execute(sql, (user,))
        results = cursor.fetchall()
        cursor.close()

    
    connection.close()
    return render_template('records.html',**locals())

@app.route("/target", methods=['GET'])
@login_required
def target():

    target = request.args.get('target')
    user = current_user.get_id()

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `records` WHERE `user`=%s AND `header`=%s ORDER BY `id` DESC  LIMIT 192"
        cursor.execute(sql, (user,target))
        results = cursor.fetchall()
        
        cursor.close()

    
    connection.close()
    return render_template('target_records.html',**locals())


@app.route("/manage", methods=['GET'])
@login_required
def manage():

    user = current_user.get_id()

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT `header`, COUNT(`header`), MAX(`time`) FROM `records` WHERE `user`=%s GROUP BY `header` ORDER BY `id` DESC"
        cursor.execute(sql, (user))
        results = cursor.fetchall()
        cursor.close()

    connection.close()
    return render_template('manage.html',**locals())


@app.route("/recorddele", methods=['GET'])
@login_required
def recorddele():
    header = request.args.get('header')
    user = current_user.get_id()

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "DELETE FROM `records` WHERE `user`=%s AND `header`=%s"
        cursor.execute(sql, (user, header))
        cursor.close()

    connection.close()
    return redirect(url_for('manage'))

#輸出csv
@app.route('/export', methods=['GET'])
def export():

    target = request.args.get('target')
    user = current_user.get_id()

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

    cw.writerow((['Target', 'Time', 'Cell', 'Tri_Loc', 'Info', 'Tri_Loc_only']))
    
    for result in results:
        cw.writerow(([result["header"],result["time"],"http://www.google.com.tw/maps/search/"+result["cell_lat"]+","+result["cell_lon"],"http://www.google.com.tw/maps/search/"+result["tri_lat"]+","+result["tri_lon"],result["msg"],result["tri_lat"]+","+result["tri_lon"]]))

    connection.close()
    response = make_response(si.getvalue())

    dt1 = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

    timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")

    disposition = "attachment; filename=output-" + user + "-" + target + "-" + timenow + ".csv"

    response.headers['Content-Disposition'] = disposition.encode('utf-8')
    response.headers["Content-type"] = "text/csv"
    return response

#登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'GET':
        return render_template("login.html")

    使用者 = request.form['user_id']

    #hash 
    s = hashlib.sha1()
    request_password = request.form['password'].encode('utf-8')
    s.update(request_password)
    request_password_h = s.hexdigest()

    #if (使用者 in users) and (request.form['password'] == users[使用者]['password']):
    if (使用者 in users) and (request_password_h == users[使用者]['password']):
        user = User()
        user.id = 使用者
        login_user(user)

        next = request.args.get('next')

        return redirect(next or url_for('show'))

    flash('登入失敗了...')
    return render_template('login.html')

#登出
@app.route('/logout')
def logout():
    使用者 = current_user.get_id()
    logout_user()
    #flash(f'{使用者}！掰掰！')
    return redirect(url_for('login'))

#
#處理即時定位 line restful insloc
#

@app.route("/insloc", methods=['GET'])
def insloc():

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `inslocs` ORDER BY `id` ASC"
        cursor.execute(sql, )
        results = cursor.fetchall()
        cursor.close()

    
    connection.close()
    return render_template('insloc.html',**locals())

@app.route("/inslocadd", methods=['POST'])
def inslocadd():

    keyword = request.form.get('keyword')
    header = request.form.get('header')
    number = request.form.get('number')
    url = request.form.get('url')
    status = request.form.get('status')

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "INSERT INTO `inslocs` (`keyword`, `header`, `number`, `url`, `status`) VALUES (%s, %s, %s, %s, %s)"
        
        cursor.execute(sql, (keyword, header, number, url, status))
        
        cursor.close()

    connection.commit()
    connection.close()
    return redirect(url_for('insloc'))


@app.route("/inslocdele", methods=['GET'])
def inslocdele():

    insloc_id = request.args.get('id')

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "DELETE FROM `inslocs` WHERE `id`=%s"
        
        cursor.execute(sql, (insloc_id))
        
        cursor.close()

    connection.commit()
    connection.close()
    return redirect(url_for('insloc'))

@app.route("/status", methods=['GET'])
def status():
    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        
        sql = "SELECT * FROM `status` WHERE `id`=4"
        cursor.execute(sql, )
        results = cursor.fetchone()
        cursor.close()

    status = results["keyword"]
    connection.close()

    return status



@app.route("/insaddnew", methods=['GET'])
def insaddnew():
    # read parameters
    msg = request.args.get('msg')
    msg2 = request.args.get('msg2')
    header = request.args.get('header')
    number = request.args.get('number')
    cell_lat = request.args.get('cell_lat')
    cell_lon = request.args.get('cell_lon')
    tri_lat = request.args.get('tri_lat')
    tri_lon = request.args.get('tri_lon')
    time = request.args.get('time')
    stat = request.args.get('stat')

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # add text value
        sql = "INSERT INTO `insrecords` (`msg`, `msg2`, `header`, `number`, `cell_lat`, `cell_lon`, `tri_lat`, `tri_lon`, `time`, `stat`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        cursor.execute(sql, (msg, msg2, header, number, cell_lat, cell_lon, tri_lat, tri_lon, time, stat))
        
        cursor.close()

    connection.commit()
    connection.close()
    return f'add new insrecord'


# //MARK: - 投單用
@app.route("/format", methods=['GET'])
def format():    
    return render_template('format.html')

# //MARK: - 投單用
@app.route("/number", methods=['GET'])
def number():    
    return render_template('number.html')

# //MARK: - 文字同串
@app.route("/oneline", methods=['GET'])
def oneline():    
    return render_template('oneline.html')

# //MARK: - 文字組合
@app.route("/combine", methods=['GET'])
def combine():    
    return render_template('combine.html')

# //MARK: - autopic
@app.route("/autopic", methods=['GET'])
def autopic():    
    return render_template('autopic.html')


@app.route("/whois", methods=['POST'])
def whois():
    ips_form = request.form.get('result')

    rows = ips_form.split("\r\n")

    ips_array = []

    for row in rows:
        ips_array.append(row.split(","))

    ips = []
    times = []
    ports = []

    for row in ips_array:
        l = len(row)

        if l == 3:
            #彙整IP
            ips.append(row[0])
            #彙整時間
            time_format = datetime.datetime.strptime(row[1], "%Y%m%d%H%M")
            times.append(time_format)
            #彙整port
            ports.append(row[2])
            
        elif l == 2:
            #彙整IP
            ips.append(row[0])
            #彙整時間
            time_format = datetime.datetime.strptime(row[1], "%Y%m%d%H%M")
            times.append(time_format)
            #彙整port
            ports.append('0')

        else:
            print("格式有誤")
            flash('格式有誤')
            return redirect(url_for('format'))

    si = io.StringIO()
    cw = csv.writer(si)

    i = 0
    
    for ip in ips:

        isp, lookup = which_isp(ip)


        if isp == '遠傳電信股份有限公司':
            start_time = times[i] - datetime.timedelta(minutes=60)
            start_time_format = start_time.strftime('%Y%m%d%H%M%S')
            end_time = times[i]
            end_time_format = end_time.strftime('%Y%m%d%H%M%S')
        else:
            start_time = times[i] - datetime.timedelta(minutes=10)
            start_time_format = start_time.strftime('%Y%m%d%H%M%S')
            end_time = times[i] + datetime.timedelta(minutes=10)
            end_time_format = end_time.strftime('%Y%m%d%H%M%S')


        if ports[i] != '0':
            ip_port = ip + ":" + ports[i]
            cw.writerow(["IP", isp, ip_port, start_time_format, end_time_format, lookup])
            i = i + 1
        else:
            cw.writerow(["IP", isp, ip, start_time_format, end_time_format, lookup])
            i = i + 1




    response = make_response(si.getvalue())

    dt1 = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

    timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")

    disposition = "attachment; filename=output-" + timenow + ".csv"

    response.headers['Content-Disposition'] = disposition.encode('utf-8')
    response.headers["Content-type"] = "text/csv"
    return response

@app.route("/getip", methods=["GET"])
@login_required
def getip():
    
    user = current_user.get_id()

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `getip` WHERE `user`=%s ORDER BY `id` DESC LIMIT 30"
        cursor.execute(sql, (user,))
        results = cursor.fetchall()
        cursor.close()

    
    connection.close()
    return render_template('getip.html',**locals())


@app.route("/getiprecords", methods=["GET"])
@login_required
def getiprecords():

    token = request.args.get('token')
    user = current_user.get_id()

    taiwanips = ['111', '210', '36', '42', '134', '123', '180', '221', '218', '58', '1', '220', '59', '113', '116', '223', '110', '140', '125', '60',
                        '202', '114', '115', '120', '182', '122', '101', '106', '61', '117', '159', '150', '27', '222', '124', '163', '39', '219', '121', '168', '118', '112', '211', '119', '139', '175', '203', '49']

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `getip` WHERE `token`=%s"
        cursor.execute(sql, (token))
        infos = cursor.fetchall()

        sql = "SELECT * FROM `getiprecords` WHERE `token`=%s ORDER BY `id` DESC"
        cursor.execute(sql, (token))
        records = cursor.fetchall()

        cursor.close()

    
    connection.close()
    return render_template('getiprecords.html',**locals())


#輸出csv
@app.route('/getipexport', methods=['GET'])
@login_required
def getipexport():

    user = current_user.get_id()
    recordid = request.args.get('recordid')

    si = io.StringIO()
    cw = csv.writer(si)

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `getiprecords` WHERE `id`=%s"
        cursor.execute(sql, (recordid))
        results = cursor.fetchone()
        
        cursor.close()
    
    connection.close()

    time_f = results["time"]
    time_f = time_f[0:4]+time_f[5:7]+time_f[8:10]+time_f[11:13]+time_f[14:16]

    ips_array = [results["ip"],time_f,results["port"]]

    ips = []
    times = []
    ports = []

    ips.append(ips_array[0])
    #彙整時間
    time_format = datetime.datetime.strptime(ips_array[1], "%Y%m%d%H%M")
    times.append(time_format)
    #彙整port
    ports.append(ips_array[2])
            

    si = io.StringIO()
    cw = csv.writer(si)

    i = 0
    
    for ip in ips:

        isp, lookup = which_isp(ip)

        if isp == '遠傳電信股份有限公司':

            start_time = times[i] - datetime.timedelta(minutes=60)
            start_time_format = start_time.strftime('%Y%m%d%H%M%S')
            end_time = times[i]
            end_time_format = end_time.strftime('%Y%m%d%H%M%S')
        else:

            start_time = times[i] - datetime.timedelta(minutes=10)
            start_time_format = start_time.strftime('%Y%m%d%H%M%S')
            end_time = times[i] + datetime.timedelta(minutes=10)
            end_time_format = end_time.strftime('%Y%m%d%H%M%S')

        if ports[i] != '0':
            ip_port = ip + ":" + ports[i]
            cw.writerow(["IP", isp, ip_port, start_time_format, end_time_format, lookup])
            i = i + 1
        else:
            cw.writerow(["IP", isp, ip, start_time_format, end_time_format, lookup])
            i = i + 1

    response = make_response(si.getvalue())

    dt1 = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

    timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")

    disposition = "attachment; filename=output-" + timenow + ".csv"

    response.headers['Content-Disposition'] = disposition.encode('utf-8')
    response.headers["Content-type"] = "text/csv"

    return response
 
@app.route("/getipadd", methods=['POST'])
def getipadd():

    user = current_user.get_id()

    target = request.form.get('target')
    dsturl = request.form.get('dsturl')
    description = request.form.get('description')

    token = secrets.token_hex(4)

    s = pyshorteners.Shortener(api_key='5f060e3091383f41f019249adbddf2928cd53b45')
    bitly_url = s.bitly.short('https://dailynewstw.herokuapp.com/news/'+token)

    dt1 = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

    timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")

    connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "INSERT INTO `getip` (`user`, `target`, `dsturl`, `token`, `description`, `time`, `bitly`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        cursor.execute(sql, (user, target, dsturl, token, description, timenow, bitly_url))
        
        cursor.close()

    connection.commit()
    connection.close()
    return redirect(url_for('getip'))


if __name__ == 'main':
    app.run(threaded=True) #啟動伺服器
