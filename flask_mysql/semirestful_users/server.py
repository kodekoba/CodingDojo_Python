from flask import Flask, render_template, request, redirect
from mysqlconn import connectToMySQL  
app = Flask(__name__)

@app.route("/users")
def index():
    mysql = connectToMySQL("restful_users")             # call the function, passing in the name of our db
    users = mysql.query_db("SELECT * FROM r_users;")    # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", users_to_html = users)

@app.route("/users/new")
def add_user():
    return render_template("create.html")

@app.route("/users/create", methods=["POST"])
def add_user_redir():
    print(request.form)

    query = "INSERT INTO r_users (first_name, last_name, email) VALUES (%(fn)s, %(ln)s, %(em)s);"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email_name"]
    }
    mysql = connectToMySQL("restful_users")
    mysql.query_db(query,data)

    return redirect("/users")

@app.route("/users/<id>")
def show_user(id):
    query = "SELECT * FROM r_users WHERE user_id = %(id)s"
    data = { "id": id }
    mysql = connectToMySQL("restful_users")
    user_info = mysql.query_db(query,data)
    print(id)
    return render_template("read.html", user_info = user_info)

@app.route("/users/<id>/edit")
def edit_user(id):
    query = "SELECT * FROM r_users WHERE user_id = %(id)s"
    data = { "id": id }
    mysql = connectToMySQL("restful_users")
    edit_info = mysql.query_db(query,data)
    print(id)
    return render_template("update.html", edit_info = edit_info)

@app.route("/users/<id>/update", methods=["POST"])
def edit_user_redir(id):
    print(request.form)

    query = "UPDATE r_users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s WHERE user_id = %(id)s"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email_name"],
        "id": id
    }
    mysql = connectToMySQL("restful_users")
    mysql.query_db(query,data)

    return redirect("/users")

@app.route("/users/<id>/destroy")
def delete_user(id):
    query = "DELETE FROM r_users WHERE user_id = %(id)s"
    data = { "id": id }
    mysql = connectToMySQL("restful_users")
    mysql.query_db(query,data)
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)