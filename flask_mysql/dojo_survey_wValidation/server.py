from flask import Flask, render_template, request, redirect, session, flash
from mysqlconn import connectToMySQL
app = Flask(__name__)
app.secret_key = "ITS YA BOI STINKY PETE"

@app.route("/")   
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def create_client():
    is_valid = True
    if len(request.form["name"]) < 1:
        is_valid = False
        flash("Please enter your name")
    if len(request.form["location"]) < 2:
        is_valid = False
        flash("Please enter your dojo location")
    if len(request.form["language"]) < 2:
        is_valid = False
        flash("Please enter your favorite language")
    if is_valid:
        print("Got Post Info")
        print(request.form)
        query = "INSERT INTO dojosurvey (fullname, location, favlang, comment) VALUES (%(fn)s, %(lo)s, %(fl)s, %(co)s);"
        data = {
            "fn" : request.form["name"],
            "lo" : request.form["location"],
            "fl" : request.form["language"],
            "co" : request.form["comment"]
        }
        session["name"] = request.form["name"]
        session["location"] = request.form["location"]
        session["language"] = request.form["language"]
        session["comment"] = request.form["comment"]
        mysql = connectToMySQL("dojosurvey")
        mysql.query_db(query,data)
        # flash("Survey form successful!")
        return redirect ("/result")
    else:
        return redirect("/")

@app.route("/result")  
def result_page():
    name_from_form = session["name"]
    location_from_form = session["location"]
    language_from_form = session["language"]
    comment_from_form = session["comment"]
    return render_template("result.html", name_on_template = name_from_form, location_on_template = location_from_form, language_on_template = language_from_form, comment_on_template = comment_from_form)

if __name__ == "__main__":
    app.run(debug=True)