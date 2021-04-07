from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    return f'Hello, Heroku!'




@app.route("/getname", methods=['GET'])
def getname():
    name = request.args.get('name')
    return render_template('get.html',**locals())


if __name__ == 'main':
    app.run() #啟動伺服器