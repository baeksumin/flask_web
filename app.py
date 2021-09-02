from flask import Flask, render_template, redirect, request, session, url_for
from data import Articles
import pymysql
from passlib.hash import pbkdf2_sha256
from functools import wraps
from pymongo import MongoClient

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gangnam'

db_connection = pymysql.connect(
	user    = 'root',
        passwd  = '12345678',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

client = MongoClient("mongodb+srv://root:1234@cluster0.pzy0t.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.gangnam
db_user = client.users

list = db.list
users = db_user.users

# 데코레이터를 붙이는 방법..? 데코레이터 함수를 만든다?
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_logged' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))   
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['email'] == '10@naver.com':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('articles'))
    return wrap


@app.route('/hello')
def hello_world():
    return 'Hello World!'
    
@app.route('/', methods = ['GET', 'POST'])
@is_logged_in
def index():
    name = "KIM"
    print(len(session))
    return render_template('index.html', data = name, user = session)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', user = session)

    else:
        username = request.form["username"]
        email = request.form["email"]
        password = pbkdf2_sha256.hash(request.form["password"])
        users.insert_one({"username":username, "email":email, "password":password})
        cursor = db_connection.cursor()

        sql_1 = f"SELECT * FROM users WHERE email = '{email}'"
        cursor.execute(sql_1)
        user = cursor.fetchone()
        print(user)

        if user == None:
            sql = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}');"
            cursor.execute(sql)
            db_connection.commit()
            return redirect('/')
        else:
            return redirect('/register')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', user = session)

    else :
        email = request.form['email']
        password = request.form['password']
        sql_1 = f"SELECT * FROM users WHERE email='{email}'"
        cursor = db_connection.cursor()
        cursor.execute(sql_1)
        user = cursor.fetchone()
        print(user)
        if user == None:
            return redirect('/login')
        else:
            result = pbkdf2_sha256.verify(password, user[3])
            if result == True:
                session['id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                session['date'] = user[4]
                session['is_logged'] = True
                print(session)
                return redirect('/')
            else :
                return redirect('/login')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/articles', methods = ['GET', 'POST'])
def articles():
    # list_data = Articles()
    cursor = db_connection.cursor()
    sql = 'SELECT * FROM list;'
    cursor.execute(sql)
    topics = cursor.fetchall()
    print(topics)

    return render_template('articles.html', data = topics, user = session)

@app.route('/detail/<ids>')
def detail(ids):
    # list_data = Articles()
    cursor = db_connection.cursor()
    sql = f'SELECT * FROM list WHERE id={int(ids)};'
    cursor.execute(sql)
    topic = cursor.fetchone()
    print(topic)
    # for data in list_data:
    #     if data['id'] == int(ids):
    #         article = data
    return render_template('article.html', article = topic, user = session)

@app.route('/add_article', methods = ['GET', 'POST'])
@is_logged_in
def add_article():
    if request.method == "GET":
        return render_template('add_article.html', user = session)

    else:
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        list.insert_one({"title":title, "description":desc, "author":author})
        cursor = db_connection.cursor()
        sql = f"INSERT INTO list (title, description, author) VALUES ('{title}', '{desc}', '{author}');"
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles')


@app.route('/edit_article/<ids>', methods = ['GET', 'POST'])
@is_logged_in
def edit_article(ids):
    if request.method == 'GET':
        cursor = db_connection.cursor()
        sql = f'SELECT * FROM list WHERE id={int(ids)};'
        cursor.execute(sql)
        topic = cursor.fetchone()
        print(topic)
        return render_template('edit_article.html', article = topic, user = session)

    else:
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]

        cursor = db_connection.cursor()
        sql = f"UPDATE list SET title= '{title}', description = '{desc}', author='{author}' WHERE (id = {int(ids)});"
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles')

    
@app.route('/delete/<ids>', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def delete(ids):
    cursor = db_connection.cursor()
    sql = f'DELETE FROM list WHERE (id = {ids});'
    cursor.execute(sql)
    db_connection.commit()
    return redirect('/articles')

if __name__ == '__main__':
    app.run( debug = True )

