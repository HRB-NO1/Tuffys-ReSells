from flask import Flask, request, render_template
import os, sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homeMeth():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def loginMeth():
    username = request.form['username']
    password = request.form['password']
    msg = dealInfo(username, password, 1)
    if msg == True:
        return render_template('login.html')
    else:
        return render_template('home.html', message = msg)

@app.route('/success', methods=['POST'])
def successMeth():
    username = request.form['username']
    password = request.form['password']
    msg = dealInfo(username, password, 2)
    if msg == True:
        return render_template('success.html')
    else:
        return render_template('login.html', message = msg)

# type：1：保存 2：查询
def dealInfo(name, pwd, type):
    msg = ""
    print(name, pwd, type)
    # 没有则建立数据库文件，有则建立连接
    db_file = os.path.join(os.path.dirname(__file__), 'dbdb.db')
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
        return "用户名和密码不能为空"
    # 查询该表格下是否有该条数据
    cursor.execute("select * from user WHERE username = '%s'" %name)
    values = cursor.fetchall()
    if values:
        for value in values:
            if value[0] == name:
                if type == 1:
                    cursor.close()
                    conn.close()
                    return "该用户名已存在，请重填注册信息。。。"
                elif type == 2 and value[1] == pwd: # 信息一致，登录成功
                    cursor.close()
                    conn.close()
                    return True
                msg = "密码错误，请重新输入"
    else: # 没有查询到数据
        if type == 1:   # 信息保存成功，可以进行登录操作
            cursor.execute("insert into user VALUES ('%s', '%s')" %(name, pwd))
            cursor.close()
            conn.commit()
            conn.close()
            return True
        else:
            msg = '没有此用户名信息，请核对。。。'
    cursor.close()
    conn.close()
    return msg

if __name__ == '__main__':
    app.run()