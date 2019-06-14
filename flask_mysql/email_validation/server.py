from flask import Flask, render_template, request, redirect, session, flash
import re       # the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')      # create a regular expression object that we'll use later
from mysqlconn import connectToMySQL
app = Flask(__name__)
app.secret_key = "YEEEEEEEEEEEEEEE"

@app.route("/")   
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_email():
    if not EMAIL_REGEX.match(request.form["email"]):
        flash("Email is not valid!")
        return redirect("/")
    
    else:
        print("Got Post Info")
        print(request.form)
        query = "INSERT INTO email (email) VALUES (%(em)s);"
        data = {
            "em" : request.form["email"]
        }
        session["s_email"] = request.form["email"]
        session["logged"] = True
        mysql = connectToMySQL("emailvalid")
        mysql.query_db(query,data)
        # flash("Survey form successful!")
        return redirect ("/success")

@app.route("/success")  
def success_page():
    fl = session["s_email"]
    if session["logged"] == True:
        flash("The email address you have entered (" + fl + ") is a VALID email address. Thank you!") # issue is that this loads after deletes
    mysql = connectToMySQL("emailvalid")
    email_list = mysql.query_db("SELECT * FROM email;")
    print(email_list)
    return render_template("success.html", all_emails = email_list)

@app.route("/delete/<id>")
def delete_email(id):
    session["logged"] = False
    query = "DELETE FROM email WHERE id = %(id)s"
    data = { "id": id }
    mysql = connectToMySQL("emailvalid")
    mysql.query_db(query,data)
    return redirect("/success")

if __name__ == "__main__":
    app.run(debug=True)