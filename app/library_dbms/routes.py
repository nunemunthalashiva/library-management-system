from library_dbms import app , mysql
from flask import render_template , request ,redirect , url_for ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date,timedelta
# returning index page when someone just opens website

@app.route('/')
@app.route("/index")
def index():
    msg=''
    return render_template("index.html",msg=msg)

# returning about page
@app.route("/about")
def about():
    return render_template("about.html")

# -------------------------------------------------------

# sorry the page u are trying is out of service
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# -------------------------------------------------------

@app.route('/student_home')
def student_home():
    msg="successfully logged in"
    return render_template('student_home.html',msg=msg)

# -------------------------------------------------------

@app.route('/teacher_home')
def teacher_home():
    msg="successfully logged in"
    return render_template('teacher_home.html',msg=msg)

# -------------------------------------------------------

@app.route('/librarian_home')
def librarian_home():
    msg="successfully logged in"
    return render_template('librarian_home.html',msg=msg)

# -------------------------------------------------------

# login page for user teacher and librarian
@app.route("/login",methods=['GET','POST'])
def login():
    msg=''
    if 'user_id' in session:
        if str(session['user_id'])[0] == '1':
            return redirect(url_for('student_home'))
        elif str(session['user_id'])[0] == '2':
            return redirect(url_for('teacher_home'))
        else:
            return redirect(url_for('librarian_home'))
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST' and 'user_id' in request.form and 'password' in request.form :
        user_id = request.form['user_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user where user_id = %s and password = %s',(user_id,password,))
        person=cursor.fetchone()
        if person:
            msg="Successfully logged in"
            session['loggedin'] = True
            session['user_id'] = person['user_id']
            if str(person['user_id'])[0] == '1':
                return redirect(url_for('student_home'))
            elif str(person['user_id'])[0] == '2':
                return redirect(url_for('teacher_home'))
            elif str(person['user_id'])[0] == '3':
                return redirect(url_for('librarian_home'))
            else:
                msg='Invalid Username!'
                return render_template('login.html',msg=msg)
        else:
            msg="Invalid username / password"
            return render_template('login.html',msg=msg)
    msg='Please fill all details'
    return render_template('login.html',msg=msg)


# ------------------------------------------------------------

@app.route("/userdisplay")
def userdisplay():
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user_id = % s', (session['user_id'], ))
        user = cursor.fetchone()
        return render_template("userdisplay.html", user = user)
    return redirect(url_for('login'))

# --------------------------------------------------------------

@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'user_id' in session:
        if request.method == 'POST' and 'password' and 'address' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            password = request.form['password']
            address = request.form['address']
            cursor.execute('SELECT * FROM user WHERE user_id = % s', (session['user_id'], ))
            user1 = cursor.fetchone()
            if not user1:
                msg = 'Account already exists !'
            else:
                cursor.execute('UPDATE user SET password = % s, address = % s  WHERE user_id = % s', (password, address, (session['user_id'], ), ))
                conn.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg = msg)
    return redirect(url_for('login'))

# ------------------------------------------------------------

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))

#adding a user
@app.route('/adduser',methods=['GET','POST'])
def adduser():
    msg=''
    if 'user_id' in session and str(session['user_id'])[0]=='3':
        if request.method == 'GET':
            return render_template('adduser.html')
        if request.method=='POST' and 'user_id' in request.form and 'password' in request.form and 'address' in request.form and 'name' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            user_id = request.form['user_id']
            name=request.form['name']
            password = request.form['password']
            address = request.form['address']
            unpaid_fees=0
            cursor.execute('SELECT * FROM user where user_id = {}'.format(user_id))
            person = cursor.fetchone()
            if person:
                msg='sorry this user exists already'
            else:
                cursor.execute('INSERT INTO user values (%s,%s,%s,%s,%s)',(user_id,password,name,address,unpaid_fees))
                conn.commit()
                msg='Successfully added user'
            return render_template('librarian_home.html',msg=msg)
        return render_template('adduser.html',msg=msg)
    msg='Sorry librarian not logged in'
    return render_template('login.html',msg=msg)


# add author
@app.route('/addauthor',methods=['GET','POST'])
def addauthor():
    msg=''
    if 'user_id' in session and str(session['user_id'])[0]=='3':
        if request.method=='GET':
            return render_template('addauthor.html')
        if request.method=='POST' and 'ISBN_number' in request.form and 'name' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            ISBN_number = request.form['ISBN_number']
            name = request.form['name']
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
    msg='librarian not logged in'
    return render_template('login.html',msg=msg)


@app.route("/addbooks",methods=['GET','POST'])

def addbooks():
    msg=''
    if 'user_id' in session and str(session['user_id'])[0]=='3':
        if request.method=='GET':
            return render_template('addbooks.html')
        if request.method=='POST' and 'ISBN_number' in request.form and 'copy_number' in request.form and 'publication_year' in request.form and 'subject' in request.form and 'title' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            cursor1 = conn.cursor()
            title = request.form['title']
            subject = request.form['subject']
            ISBN_number = request.form['ISBN_number']
            publication_year = request.form['publication_year']
            copy_number = request.form['copy_number']
            cursor.execute('SELECT * FROM books where ISBN_number = %s ',(ISBN_number,))
            auth=cursor.fetchone()
            if auth:
                cursor.execute('UPDATE books SET copy_number = %s where ISBN_number = %s',(copy_number,ISBN_number,))
                conn.commit()
                msg='successfully updated quantity of books'
            else:
                cursor1.execute('SELECT * from author where ISBN_number= %s',(ISBN_number,))
                valid = cursor1.fetchone()
                if valid:
                    cursor.execute('INSERT INTO books values (%s,%s,%s,%s,%s)',(title,publication_year,copy_number,subject,ISBN_number,))
                    conn.commit()
                    msg='Successfully added books'
                else:
                    msg="Sorry first please add book inauthor"
                    return render_template("addauthor.html",msg=msg)
            return render_template('addbooks.html',msg=msg)
        return render_template('librarian_home.html',msg=msg)
    msg="Sorry librarian not logged in"
    return render_template('login.html',msg=msg)

@app.route("/booksplace",methods=['GET','POST'])
def booksplace():
    msg=''
    if 'user_id' in session and str(session['user_id'])[0]=='3':
        if request.method=='POST' and 'shelf_id' in request.form and'ISBN_number' in request.form and 'book_quantity' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            shelf_id = request.form['shelf_id']
            ISBN_number = request.form['ISBN_number']
            book_quantity = request.form['book_quantity']
            cursor.execute('SELECT * FROM books_place where shelf_id = %s ',(shelf_id,))
            auth=cursor.fetchone()
            if auth:
                cursor.execute('UPDATE books_place SET book_quantity = %s where ISBN_number = %s and shelf_id = %s ',(book_quantity,ISBN_number,shelf_id))
                conn.commit()
                msg='successfully updated quantity of books'
            else:
                msg='sorry this ISBN_number or shelf id doesnt seem to exists please add ISBN first'
                return render_template('booksplace.html',msg=msg)
            return render_template('librarian_home.html',msg=msg)
        msg="Sorry please try again"
        return render_template('addbooks.html',msg=msg)
    msg="Sorry librarian not logged in"
    return render_template('login.html',msg=msg)

#-----------order_books---------

@app.route('/order_books',methods=['GET','POST'])
def order_books():
    msg=''
    if 'user_id' in session and (str(session['user_id'])[0] == '1' or str(session['user_id'])[0]== '2'):
        if request.method=='GET':
            return render_template("order_books.html",msg=msg)
        if request.method=='POST' and 'ISBN_number' in request.form and 'status' in request.form :
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            user_id = session['user_id']
            ISBN_number = request.form['ISBN_number']
            status = request.form['status']
            date_booked = date.today()
            due_date = date.today()
            if (str(session['user_id'])[0])=='1':
                due_date = date_booked + timedelta(days=+10)
            else:
                due_date = date_booked + timedelta(days=+1000000000)
            cursor.execute("SELECT * FROM books WHERE ISBN_number=(%s)",(ISBN_number,))
            ISBN_numbers=cursor.fetchone()
            if ISBN_numbers:
                cursor.execute(("select ((select copy_number from books where ISBN_number=(%s))-(select count(*) from order_books where status_of_book<>(%s) and ISBN_number=(%s))) as Difference"),(ISBN_number,'on_shelf',ISBN_number,))
                avaliable_books = cursor.fetchone()
                if avaliable_books:
                    cursor.execute("INSERT INTO order_books VALUES(%s,%s,%s,%s,%s)",(user_id,ISBN_number,status,date_booked,due_date,))
                    mysql.connection.commit()
                    msg='ordered successfully'
                    return render_template('order_books.html',msg=msg)
                msg='this book is not available'
                return render_template('order_books.html',msg=msg)
            msg='invalid isbn number'
            return render_template('order_books.html',msg=msg)
        msg='please fillout form completely'
        return render_template('order_books.html',msg=msg)
    msg='please login first'
    return render_template('login.html',msg=msg)

#---------------------------add_to_cart----------------------------------------------------------
@app.route('/add_to_cart',methods=['GET','POST'])
def add_to_cart():
    msg=''
    if 'user_id' in session and (str(session['user_id'])[0] == '1' or str(session['user_id'])[0]== '2'):
        if request.method=='GET':
            return render_template("add_to_cart.html")
        if request.method=='POST' and 'ISBN_number' in request.form:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            user_id = session['user_id']
            ISBN_number = request.form['ISBN_number']
            cursor.execute("SELECT * FROM books WHERE ISBN_number=(%s)",(ISBN_number,))
            ISBN_numbers=cursor.fetchone()
            if ISBN_numbers:
                cursor.execute("SELECT * FROM add_to_cart WHERE user_id=(%s) and ISBN_number=(%s)",(user_id,ISBN_number,))
                already_added = cursor.fetchone()
                if already_added:
                    msg = "you have alredy added it to the cart"
                    return render_template("add_to_cart.html",msg=msg)
                cursor.execute("INSERT INTO add_to_cart VALUES(%s ,%s)",(user_id,ISBN_number,))
                mysql.connection.commit()
                msg='successfully added to cart'
                return render_template("add_to_cart.html",msg=msg)
            msg="please use valid isbn number"
            return render_template("add_to_cart.html",msg=msg)
        msg='First,fill out isbn number'
        return render_template('add_to_cart.html',msg=msg)
    msg='please login first'
    return render_template('login.html',msg=msg)

#----------------------------review------------------------
@app.route('/review',methods=['GET','POST'])
def review():
    msg=''
    if 'user_id' in session and (str(session['user_id'])[0] == '1' or str(session['user_id'])[0]== '2'):
        if request.method=='GET':
            return render_template("review.html")
        if request.method=='POST' and 'ISBN_number' in request.form and 'rating' in request.form and 'discription' in request.form:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            user_id = session['user_id']
            ISBN_number = request.form['ISBN_number']
            rating = request.form['rating']
            discription = request.form['discription']
            cursor.execute("SELECT * FROM books WHERE ISBN_number=(%s)",(ISBN_number,))
            ISBN_numbers=cursor.fetchone()
            if ISBN_numbers:
                on_hold='on_hold'
                cursor.execute("SELECT * FROM order_books WHERE user_id=(%s) AND ISBN_number=(%s) AND status_of_book<>(%s)",(user_id,ISBN_number,on_hold,))
                present = cursor.fetchone()
                if present:
                    cursor.execute("SELECT * FROM review WHERE user_id=(%s) and ISBN_number=(%s)",(user_id,ISBN_number,))
                    already_added = cursor.fetchone()
                    if already_added:
                        msg="you have alredy reviewed this book"
                        return render_template("review.html",msg=msg)
                    cursor.execute("INSERT INTO review VALUES(%s ,%s, %s, %s)",(user_id,ISBN_number,rating,discription,))
                    mysql.connection.commit()
                    msg='review recorded succesfully'
                    return render_template("review.html",msg=msg)
                msg = 'you havent read that book yet!'
                return render_template("review.html",msg=msg)
            msg="please use valid isbn number"
            return render_template("review.html",msg=msg)
        msg='First,fill out complete form'
        return render_template('review.html',msg=msg)
    msg='please login first'
    return render_template('login.html',msg=msg)

#------------------------------recommendations--------------
@app.route('/recommendations')
def recommendations():
    msg=''
    if 'user_id' in session and (str(session['user_id'])[0] == '1' or str(session['user_id'])[0]== '2'):
        user_id = session['user_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT books.subject FROM review INNER JOIN books ON review.ISBN_number = books.ISBN_number WHERE user_id=(%s) AND rating > %s",(user_id,3,))
        subjects = cursor.fetchone()
        if subjects:
            cursor.execute("SELECT * FROM books WHERE subject= (%s)",(subjects,))
            recommended_books = cursor.fetchall()
            if recommended_books:
                msg = 'these are ur recommendations and good reviewed books'
                return render_template('recommendations.html',msg=msg,recommended_books = recommended_books)
        msg="no recommendations till date"
        return render_template('recommendations.html',msg = msg)
    msg='please login first'
    return render_template('login.html',msg=msg)


#-check_shelf--------------------

@app.route('/check_shelf')
def check_shelf():
    msg = ''
    if 'user_id' in session and str(session['user_id'])[0]!='3':
        user_id = session['user_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM books WHERE ISBN_number IN (SELECT ISBN_number FROM add_to_cart WHERE user_id=(%s))",(user_id,))
        books=cursor.fetchall()
        if books:
            msg = "these are all your saved books"
            return render_template('check_shelf.html',books=books,msg = msg)
        msg = 'no books saved to your cart yet'
        return render_template('check_shelf.html',msg=msg)
    msg = 'please login first'
    return render_template('login.html',msg=msg)



#-------------check_review-----------

@app.route('/check_review',methods=['GET','POST'])
def check_review():
    msg=''
    if 'user_id' in session and str(session['user_id'])[0]!='3':
        if request.method == 'GET':
            return render_template("check_review.html")
        if 'ISBN_number' in request.form:
            ISBN_number = request.form['ISBN_number']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM books WHERE ISBN_number = (%s)",(ISBN_number,))
            valid = cursor.fetchone()
            if valid:
                cursor.execute("SELECT * FROM review WHERE ISBN_number= (%s)",(ISBN_number,))
                reviews = cursor.fetchall()
                msg = " review of this book "
                return render_template('check_review_2.html',reviews=reviews,msg=msg)
            msg = 'invalid isbn number/no such books present in library'
            return render_template('check_review.html',msg=msg)
        msg = 'please enter isbn number'
        return render_template("check_review.html",msg=msg)
    msg = "please login first"
    return render_template("login.html",msg=msg)

#-------------------books gallery--
@app.route('/books_gallery')
def books_gallery():
    return render_template('books_gallery.html')
