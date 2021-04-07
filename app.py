
from flask import Flask, request, abort, render_template

@app.route("/getname", methods=['GET'])

def getname():
    name = request.args.get('name')
    return render_template('get.html',**locals())