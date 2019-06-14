from flask import Flask, render_template, request, redirect, session, flash
import re
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
from mysqlconn import connectToMySQL
app = Flask(__name__)
app.secret_key = "YEEEEEEEEEEEEEEE"
bcrypt = Bcrypt(app)

@app.route("/")   
def index():
    if not "loggedout" in session.keys():
        session["loggedout"] = False
    if session["loggedout"] == True:
        flash("You have been successfully logged out.", "logout")
    session["loggedout"] = False
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    is_valid = True       # include some logic to validate user input before adding them to the database!
    if len(request.form["fname"]) == 0:
        is_valid = False
        flash("This is a required field", "fname")
    elif len(request.form["fname"]) < 2:
        is_valid = False
        flash("First name must be at least 2 characters", "fname")
    elif not NAME_REGEX.match(request.form["fname"]):
        is_valid = False
        flash("First name must contain only letters", "fname")
    if len(request.form["lname"]) == 0:
        is_valid = False
        flash("This is a required field", "lname")
    elif len(request.form["lname"]) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters", "lname")
    elif not NAME_REGEX.match(request.form["lname"]):
        is_valid = False
        flash("Last name must contain only letters", "lname")
    if len(request.form["email"]) == 0:
        is_valid = False
        flash("This is a required field", "email")
    elif not EMAIL_REGEX.match(request.form["email"]):
        is_valid = False
        flash("Invalid email address!!", "email")
    if len(request.form["pass"]) == 0:
        is_valid = False
        flash("This is a required field", "pass")
    elif len(request.form["pass"]) < 8:
        is_valid = False
        flash("Password must be at least 8 characters!!", "pass")
        # Ninja Bonus: Make pw HAVE to contain an uppercase letter and a special character
    if request.form["pass2"] != request.form["pass"]:
        is_valid = False
        flash("Passwords must match!!", "pass2")
    if is_valid:
        print("Got Post Info")
        print(request.form)
        session["first"] = request.form["fname"]
        session["justregistered"] = True
        pw_hashed = bcrypt.generate_password_hash(request.form['pass'])  # create the hash
        print(pw_hashed)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'
        mysql = connectToMySQL("loginregi")
        query = "INSERT INTO users (first_name, last_name, user_email, pw_hash) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s);"
        # put the pw_hash in our data dictionary, NOT the password the user provided
        data = { 
            "fn" : request.form["fname"],
            "ln" : request.form["lname"],
            "em" : request.form["email"],
            "pw" : pw_hashed 
        }
        mysql.query_db(query, data)
        return redirect("/success")    #later flash success using a session call
    else:
        # flash("User creation failed")
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    if len(request.form["loginemail"]) == 0:
        flash("This is a required field", "logemail")
    if len(request.form["loginpass"]) == 0:
        flash("This is a required field", "logpass")

    # see if the username provided exists in the database
    mysql = connectToMySQL("loginregi")
    query = "SELECT * FROM users WHERE user_email = %(em)s;"
    data = { "em" : request.form["loginemail"] }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['pw_hash'], request.form['loginpass']):
            # if we get True after checking the password, we may put the user id in session
            session["userid"] = result[0]["user_id"]
            # session["first"] = result[0]["first_name"]
            return redirect('/success')
    flash("You could not be logged in", "loginfail")
    return redirect("/")


@app.route("/success")
def login_success():
    # if not "justlogged" in session.keys(): 
    #     session["justlogged"] = False
    # if session["justlogged"] == True:
    #     flash("Welcome back, " + session["first"])

    # for using a session key to store first name
        # if not "first" in session.keys():
        #     session["first"] = False

    if not "justregistered" in session.keys():
        session["justregistered"] = False
    if session["justregistered"] == True:
        flash("Thank you for registering with us " + session["first"])

    # for referencing the first name through MySQL and a session key
    if not "userid" in session.keys():
        session["userid"] = False
    mysql = connectToMySQL("loginregi")
    query = "SELECT first_name FROM users WHERE user_id = %(id)s;"
    data = { "id" : session["userid"] }
    fn_output = mysql.query_db(query, data)
    return render_template("success.html", fn_from_mysql = fn_output)

    # return render_template("success.html")
    
@app.route("/logout")
def delcookies():
    session.clear()
    session["loggedout"] = True
    # session.clear()		    # clears all keys
    # session.pop('key_name')	# clears a specific key
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)