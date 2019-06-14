from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = "sshh"
bcrypt = Bcrypt(app)
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/register', methods=['POST'])
def reg():
    mysql = connectToMySQL('favoritebook')
    query = "select * from users where username = %(username)s"
    data = {
        'username' : request.form['username']
    }
    usernamecheck = mysql.query_db(query,data)
    print(usernamecheck)

    is_valid = True 
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("Please enter valid first name",'ferror')
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Please end valid last name",'lerror')
    if not email_regex.match(request.form['email_entered']):
        is_valid = False
        flash("Invalid email address",'eerror')
    if len(request.form['password_entered']) < 5:
        is_valid = False
        flash("Password is too short",'perror')
    if len(usernamecheck) > 0:
        is_valid = False
        flash("This Username already in use!!!!! :(",'uerror')
    if request.form['password_entered'] != request.form['confirmed_password']:
        is_valid = False
        flash("Confirmation password does NOT match password",'cperror')

    if not is_valid:
        return redirect('/')

    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password_entered'])
        mysql = connectToMySQL("favoritebook")
        query = "insert into users (first_name, last_name, username, email, password, enabled, created_on, updated_on) values (%(first_name_entered)s, %(last_name_entered)s, %(username)s, %(email_entered)s, %(password_entered)s, 1, now(), now());"
        data = {
            'first_name_entered' : request.form['first_name'],
            'last_name_entered' : request.form['last_name'],
            'username' : request.form['username'],
            'email_entered' : request.form['email_entered'],
            'password_entered' : pw_hash
        }
        print(query)
        registered_id = mysql.query_db(query,data)
        mysql = connectToMySQL("favoritebook")
        query = "select * from users where id = %(registered_id)s"
        data = {
            "registered_id" : registered_id
        }
    log = mysql.query_db(query,data)
    session['user'] = log
    return redirect('/books')




@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('favoritebook')
    query = "select * from users where email = %(email_input)s; "
    data = {
        "email_input" : request.form["email_login"]
    }
    result = mysql.query_db(query,data)
    print(result)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password_login']):
            session['user'] = result 
            return redirect('/books')
    flash("You could not be logged in","loginerror")
    return redirect('/')


@app.route('/books')
def wall():
    mysql = connectToMySQL('favoritebook')
    query = """select 
        books.id,
        books.title,
        books.description,
        users.first_name,
        users.last_name,
        users.username
        from favoritebook.books books
        join favoritebook.users users on users.id = books.uploaded_by
        where books.enabled = 1;"""
    addedbooks = mysql.query_db(query)


    mysql = connectToMySQL('favoritebook')
    query = """select 
        users.id,
        users.first_name,
        users.last_name,
        users.username,
        books.id as 'bookid',
        books.title as 'favbooks'
        from favoritebook.users users
        left join favoritebook.favorites fav on fav.user_id = users.id
        left join favoritebook.books books on books.id = fav.book_id; """
    favbooks = mysql.query_db(query)

    return render_template('books.html', addedbooks = addedbooks, favbooks = favbooks)



@app.route('/addbook', methods=['POST'])
def addbook():
    is_valid = True 
    if len(request.form['book_title']) < 1:
        is_valid = False 
        flash("Book title is required","berror")
    if len(request.form['book_desc']) < 6:
        is_valid = False
        flash("Please use more words to describe this awesome book!")
    
    if not is_valid:
        return redirect('/books')

    else:
        mysql = connectToMySQL('favoritebook')
        query = "insert into books (title, description, enabled, created_on, updated_on, uploaded_by) values(%(booktitle)s, %(bookdescription)s, 1, now(), now(), %(uploader)s); "
        data = {
            'booktitle' : request.form['book_title'],
            'bookdescription' : request.form['book_desc'],
            'uploader' : session['user'][0]['id']
        }
        addbook = mysql.query_db(query,data)

        mysql = connectToMySQL('favoritebook')
        favquery = "insert into favorites (user_id, book_id) values (%(userid)s, %(bookid)s); "
        favdata = {
            'userid' : session['user'][0]['id'],
            'bookid' : addbook
        }
        mysql.query_db(favquery,favdata)

        return redirect('/books')




@app.route('/books/<id>')
def inspect(id):
    mysql = connectToMySQL('favoritebook')
    query = """select 
        books.id,
        books.title,
        users.username,
        books.created_on,
        books.updated_on,
        books.description,
        books.uploaded_by,
        users.id as 'userid'
        from favoritebook.books books
        join favoritebook.users users on users.id = books.uploaded_by
        where books.id = %(id)s ; """
    data = {
        'id' : id
    }
    inspectbooks = mysql.query_db(query,data)

    mysql = connectToMySQL('favoritebook')
    query = """select 
        users.id as 'userid',
        users.first_name,
        users.last_name,
        users.username,
        books.id as 'bookid',
        books.title as 'favbooks',
        fav.user_id as fav_user_id,
        fav.book_id as fav_book_id
        from favoritebook.users users
        left join favoritebook.favorites fav on fav.user_id = users.id
        left join favoritebook.books books on books.id = fav.book_id 
        where books.id = %(id)s;  """
    data = {
        'id' : id
    }
    favoritebooks = mysql.query_db(query,data)
    print(favoritebooks)

    mysql = connectToMySQL('favoritebook')
    query = "select user_id, book_id from favorites where user_id = %(userid)s and book_id = %(bookid)s ;"
    data = {
        'userid' : session['user'][0]['id'],
        'bookid' : id
    }
    favoritelists = mysql.query_db(query,data)
    print(favoritelists,"*"*100)
    isempty = False
    if not favoritelists:
       isempty = True

    return render_template('inspect.html', inspectbooks = inspectbooks, favoritebooks = favoritebooks, favoritelists = favoritelists, isempty = isempty)



@app.route('/update/<id>', methods=['POST'])
def update(id):
    mysql = connectToMySQL('favoritebook')
    query = "update books set description = %(description)s ,updated_by = %(id)s where id = %(bookid)s ;"
    data = {
        'description' : request.form['description_update'],
        'id' : session['user'][0]['id'],
        'bookid' : request.form['book_id']
    }
    mysql.query_db(query,data)
    flash("Description has been updated!!!","dupdate")

    return redirect(f"/books/{id}")



@app.route('/delete', methods=['POST'])
def delete():
    mysql = connectToMySQL('favoritebook')
    query = "update books set enabled = 0 where id = %(bookid)s ;"
    print(request.form)
    data = {
        'bookid' : request.form['book_id']
    }
    mysql.query_db(query,data)

    return redirect('/books')


@app.route('/unfavorite/<id>', methods=['POST'])
def unfav(id):
    mysql = connectToMySQL('favoritebook')
    query = "delete from favorites where user_id = %(userid)s and book_id = %(bookid)s "
    data = {
        'userid' : session['user'][0]['id'],
        'bookid' : request.form['favbookid']
    }
    mysql.query_db(query,data)
    return redirect(f"/books/{id}")


@app.route('/favorite/<id>', methods=['POST'])
def fav(id):
    mysql = connectToMySQL('favoritebook')
    query = "insert into favorites (user_id, book_id) values (%(userid)s, %(bookid)s);"
    data = {
        'userid' : session['user'][0]['id'],
        'bookid' : request.form['favbookid']
    }
    mysql.query_db(query,data)
    return redirect(f"/books/{id}")



@app.route('/logout')
def logout():
    session['user'] = None
    session.clear()
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)
