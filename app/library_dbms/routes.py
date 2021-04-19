from library_dbms import app , mysql
from flask import render_template , request ,redirect , url_for ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors

# returning index page when someone just opens website
@app.route("/")
def index():
    msg=''
    if 'user_id' in session:
        msg='Already logged in returning to home page'
        if str(session['user_id'])[0]==1:
            return render_template("student_home.html",msg=msg)
        elif str(session['user_id'])[0] == 2:
            return render_template("teacher_home.html",msg=msg)
        return render_template("librarian_home.html",msg=msg)
    return render_template("index.html",msg=msg)

# returning about page
@app.route("/about")
def about():
    return render_template("about.html")

# sorry the page u are trying is out of service
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# login page for user teacher and librarian
@app.route("/login",methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST' and 'user_id' in request.form and 'password' in request.form :
        user_id = request.form['user_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user where user_id = %d and password = %s',(user_id,password))
        person=cursor.fetchone()
        if person:
            msg="Successfully logged in"
            session['loggedin'] = True
            session['user_id'] = person['user_id']
            if str(person['user_id'])[0] == 1:
                return render_template(student_home.html,msg=msg)
            elif str(person['user_id'])[0] == 2:
                return render_template(teacher_home.html,msg=msg)
            elif str(person['user_id'])[0] == 3:
                return render_template(librarian_home.html,msg=msg)
            else:
                msg='Invalid Username!'
        else:
            msg="Invalid username  password"
            return render_template('login.html',msg=msg)
        msg='Please fill all details'
    return render_template('login.html',msg=msg)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))

#adding a user
@app.route('/adduser',methods=['GET','POST'])
def adduser():
    msg=''
    if session['loggedin'] == True and str(session['user_id'])[0] =='2':
        if request.method=='POST' and 'user_id' in request.form and 'password' in request.form and 'address' in request.form and 'name' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            user_id = request.form['user_id']
            name=request.form['name']
            password = request.form['password']
            address = request.form['address']
            unpaid_fees=0
            cursor.execute('SELECT * FROM user where user_id = %d',(user_id,))
            person = cursor.fetchone()
            if person:
                msg='sorry this user exists already'
            else:
                cursor.execute('INSERT INTO user values (%d,%s,%s,%s,%d)',(user_id,password,name,address,unpaid_fees))
                conn.commit()
                msg='Successfully added user'
                return render_template('librarian_home.html',msg=msg)
            return render_template('adduser.html',msg=msg)
        msg='Please try again'
        return render_template('adduser.html',msg=msg)
    msg='Librarian is not logged in'
    return render_template('login.html',msg=msg)

# add author
@app.route('/addauthor',methods=['GET','POST'])
def addauthor():
    msg=''
    if session['loggedin'] == True and str(session['user_id'])[0] =='2':
        if request.method=='POST' and 'ISBN_number' in request.form and 'name' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            ISBN_number = request.form['ISBN_number']
            name = request.form['author']
            cursor.execute('SELECT * FROM author where ISBN_number = %s and name = %s',(ISBN_number,name))
            auth = cursor.fetchone()
            if auth:
                msg='sorry this author and ISBN_number exists already'
            else:
                cursor.execute('INSERT INTO author values (%s,%s)',(ISBN_number,name))
                conn.commit()
                msg='Successfully added author and corresponding book'
                return render_template('librarian_home.html',msg=msg)
            return render_template('addauthor.html',msg=msg)
        msg='please try again'
        return render_template('addauthor.html',msg=msg)
    msg='Librarian is not logged in'
    return render_template('login.html',msg=msg)

@app.route("/addbooks",methods=['GET','POST'])

def addbooks():
    msg=''
    if session['loggedin'] ==True and str(session['user_id'])[0]=='2':
        if request.method=='POST' and 'ISBN_number' in request.form and 'copy_number' in request.form and 'publication_year' in request.form and 'subject' in request.form and 'tile' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            title = request.form['title']
            subject = request.form['subject']
            ISBN_number = request.form['ISBN_number']
            publication_year = request.form['publication_year']
            copy_number = request.form['copy_number']
            cursor.execute('SELECT * FROM books where ISBN_number = %s ',(ISBN_number,))
            auth=cursor.fetchone()
            if auth:
                cursor.execute('UPDATE books SET copy_number = %s where ISBN_number = %s',(copy_number,ISBN_number))
                conn.commit()
                msg='successfully updated quantity of books'
            else:
                cursor.execute('INSERT INTO books values (%s,%s,%d,%s)',(title,publication_year,copy_number,subject))
                msg='Successfully added books'
                return render_template('addbooks.html',msg=msg)
            return render_template('librarian_home.html',msg=msg)
        msg="Sorry please try again"
        return render_template('addbooks.html',msg=msg)
    msg="Sorry librarian not logged in"
    return render_template('login.html',msg=msg)

@app.route("/booksplace",methods=['GET','POST'])
def booksplace():
    msg=''
    if session['loggedin'] ==True and str(session['user_id'])[0]=='2':
        if request.method=='POST' and 'shelf_id' in request.form and'ISBN_number' in request.form and 'book_quantity' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            shelf_id = request.form['shelf_id']
            ISBN_number = request.form['ISBN_number']
            book_quantity = request.form['book_quantity']
            cursor.execute('SELECT SUM(book_quantity) FROM books_place where shelf_id = %s ',(ISBN_number,))
            auth=cursor.fetchone()
            if auth:
                cursor.execute('UPDATE books SET copy_number = %s where ISBN_number = %s',(copy_number,ISBN_number))
                conn.commit()
                msg='successfully updated quantity of books'
            else:
                msg='sorry this ISBN_number or shelf id doesnt seem to exists please add ISBN first'
                return render_template('addauthor.html',msg=msg)
            return render_template('librarian_home.html',msg=msg)
        msg="Sorry please try again"
        return render_template('addbooks.html',msg=msg)
    msg="Sorry librarian not logged in"
    return render_template('login.html',msg=msg)
