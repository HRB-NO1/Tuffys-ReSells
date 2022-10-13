#!/usr/bin/env python3

from flask import Flask, request, render_template
import os, sqlite3

app = Flask(__name__)



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
        cursor.execute('create table user(username VARCHAR(20), password VARCHAR(20))')
    # 判断用户名和密码是否为空
    if name == '' or pwd == '':
        return "Username and password can not be empty"
    # 查询该表格下是否有该条数据
    cursor.execute("select * from user WHERE username = '%s'" %name)
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
            cursor.execute("insert into user VALUES ('%s', '%s')" %(name, pwd))
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
    app.run()