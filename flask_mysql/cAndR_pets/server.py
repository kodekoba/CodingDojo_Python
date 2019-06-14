from flask import Flask, render_template, request, redirect
from mysqlconn import connectToMySQL  # import the function that will return an instance of a connection
app = Flask(__name__)

@app.route("/")
def index():
    mysql = connectToMySQL('pets')             # call the function, passing in the name of our db
    petslist = mysql.query_db('SELECT * FROM pets;')  # call the query_db function, pass in the query as a string
    print(petslist)
    return render_template("index.html", all_pets = petslist)

@app.route("/add_pet", methods=["POST"])
def add_pet_to_db():
    print(request.form)
    
    query = "INSERT INTO pets (name, type) VALUES (%(na)s, %(ty)s);"
    data = {
        "na": request.form["name"],
        "ty": request.form["type"]
    }
    db = connectToMySQL("pets")
    db.query_db(query,data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)