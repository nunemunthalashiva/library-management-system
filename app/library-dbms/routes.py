from library-dbms import app , mysql
from flask import render_template , request ,redirect , url_for ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors

# returning index page when someone just opens website
@app.route("/")
def index():
    msg=''
    if 'user_id' in session:
        msg='Already logged in returning to home page'
        if str(session['user_id'])[1]==1:
            return render_template(student_home.html,msg=msg)
        elif str(session['user_id'])[0] == 2:
            return render_template(teacher_home.html,msg=msg)
        return render_template(librarian_home.html,msg=msg
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
        cursor.execute('select * from patient where user_id = %d and password = %s',(user_id,password))
        person=cursor.fetchone()
        if person:
            msg='Successfully logged in'
            session['loggedin'] = True
            session['user_id'] = person['user_id']
            if str(person['user_id'])[0] == 1:
                return render_template(student_home.html,msg=msg)
            elif str(person['user_id'])[0] == 2:
                return render_template(teacher_home.html,msg=msg)
            elif str(person['user_id'])[0] == 3:
                return render_template(librarian_home.html,msg=msg)
            else:
                msg="Invalid Username!"
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

@app.route('add_user')
def adduser():
    msg=''
    if session['loggedin'] == True and str(session['user_id'])[0]='2':
        if request.method=='POST' and 'user_id' in request.form and 'password' in request.form and 'address' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            user_id = request.form['user_id']
            password = request.form['password']
            address = request.form['address']
            cursor.execute('SELECT * FROM user where user_id = %d',(user_id,))
            person = cursor.fetchone()
            if person:
                msg='sorry this user exists already'
            else:
                cursor.execute('INSERT INTO user values (%s,%s,%s)',(user_id,password,address))
                conn.commit()
                msg='Successfully added users'
                return redirect(url_for('librarian_home.html'))
            return render_template('adduser.html',msg=msg)
        msg='Please try again'
        return render_template('add_user.html',msg=msg)
    msg='Librarian is not logged in'
    return render_template('add_user.html',msg=msg)
