from flask import Flask, render_template    #added render_template     # Import Flask to allow us to create our app
app = Flask(__name__)       # Create a new instance of the Flask class called "app"

# @app.route("/")             # The "@" decorator associates this route with the function
# def hello_world():          
#     # return "Hello World!"   # Return this string response
#     return render_template("index.html") # h1 rendered response

@app.route("/")
def hello_index():
    return render_template("index.html", phrase = "hello", times = 5) # notice the 2 new named arguments!


@app.route("/name")            
def hello_me():          
    return "Hello YUNGSWAZZY9000!"

@app.route("/akiko")            
def hello_you():          
    return "Hi akiko nwn"

# @app.route("/<name>")            
# def hello_person(name):
#     print("*"*80)
#     print("in hello_person function")
#     print(name)    
#     return f"hallo {name}!"
#     # return "Hello, " + name

@app.route("/hello/<name>")            
def hello_person(name):
    print("*"*80)
    print("in hello/<name> function")
    print(name)    
    return render_template("name.html", some_name=name) 

@app.route("/users/<username>/<id>")    # for a route '/users/____/____', two parameters in the url get passed as username and id
def show_user_profile(username, id):
    print(username)
    print(id)
    return "USERNAME: " + username + ", ID: " + id

@app.route("/success")
def success():
    return "S U C C E S S"

@app.route("/lists")
def render_lists():
    student_info = [
       {'name' : 'Michael', 'age' : 35},
       {'name' : 'John', 'age' : 30 },
       {'name' : 'Mark', 'age' : 25},
       {'name' : 'KB', 'age' : 27}
    ]
    return render_template("lists.html", random_numbers = [3,1,5], students = student_info)


if __name__ == "__main__":  # Ensure this file is being run directly and not from a different module
    app.run(debug = True)   # Run the app in debug mode


