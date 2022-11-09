#!/usr/bin/env python3
# coding:utf-8
#pip install sqlalchemy
#pip install flask_sqlalchemy

from flask import Flask, request, render_template
import os, sqlite3
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time

from datetime import timedelta

 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 


app = Flask(__name__)

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET'])
def signin_page():
    return render_template('sign.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    msg = dealInfo(username, password, 2)
    if msg == True:
        return render_template('main.html',username = username)
    else:
        return render_template('sign.html', message = msg)

@app.route('/sign_up/', methods=['GET'])
def signup_page():
    return render_template('sign_up.html')

@app.route('/sign_up/', methods=['POST'])
def sign_up():
    username = request.form['username']
    password = request.form['password']
    msg = dealInfo(username, password, 1)
    if msg == True:
        return render_template('sign.html')
    else:
        return render_template('sign_up.html', message = msg)

@app.route('/admin', methods=['POST', 'GET'])
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   cur.execute("select * from user")
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "only png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', user_input + ".jpg"), img)
 
        return render_template('upload_ok.html',userinput=user_input,val1=time.time())
 
    return render_template('upload.html')


# type：1：保存 2：查询
def dealInfo(name, pwd, type):
    msg = ""
    print(name, pwd, type)
    # 没有则建立数据库文件，有则建立连接
    db_file = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # 获取该数据库下的所有表名
    a = "select name from sqlite_master where type = 'table'"
    cursor.execute(a)
    tableNames = cursor.fetchall()
    # 若无表，则新建表格'user'
    if tableNames:
        pass
    else:
        cursor.execute('create table user(username VARCHAR(20), password VARCHAR(20), certificate INT(1))')
    # 判断用户名和密码是否为空
    if name == '' or pwd == '':
        return "Username and password can not be empty"
    # 查询该表格下是否有该条数据
    cursor.execute("select username, password from user WHERE username = '%s'" %name)
    values = cursor.fetchall()
    if values:
        for value in values:
            if value[0] == name:
                if type == 1:
                    cursor.close()
                    conn.close()
                    return "This username has exist"
                elif type == 2 and value[1] == pwd: # 信息一致，登录成功
                    cursor.close()
                    conn.close()
                    return True
                msg = "Wrong password, please re-enter..."
    else: # 没有查询到数据
        if type == 1:   # 信息保存成功，可以进行登录操作
            cursor.execute("insert into user VALUES ('%s', '%s', 0)" %(name, pwd))
            cursor.close()
            conn.commit()
            conn.close()
            return True
        else:
            msg = 'No such username information, please check...'
    cursor.close()
    conn.close()
    return msg



if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)