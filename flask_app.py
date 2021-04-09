from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

import pymysql
import pymysql.cursors


app = Flask(__name__)
bootstrap = Bootstrap(app)

# Connect to the database
connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    # Create a new record
    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

connection.commit()




@app.route('/')
def hello():
    return f'Hello, Heroku!'




@app.route("/getname", methods=['GET'])
def getname():
    name = request.args.get('name')
    return render_template('get.html',**locals())


@app.route("/addnew", methods=['GET'])
def addnew():
    with connection.cursor() as cursor:
        # add text value
        sql = "INSERT INTO `records` (`header`, `user`, `msg`, `cell_lat`, `cell_lon`, `tri_lat`, `tri_lon`, `url`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, ('即時定位測試', 'chun', '訂位成功', '23', '123', '23', '123', 'http://ggfdg.com'))
    
@app.route("/show", methods=['GET'])
def show():
    with connection.cursor() as cursor:
        sql = "SELECT `header`, `msg` FROM `records` WHERE `user`=%s"
        cursor.execute(sql, ('chun',))
        result = cursor.fetchone()
        print(result)
    return f'Hello, Heroku {result["user"]}!'


if __name__ == 'main':
    app.run() #啟動伺服器