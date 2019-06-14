from flask import Flask     # Import Flask to allow us to create our app
app = Flask(__name__)       # Create a new instance of the Flask class called "app"

@app.route("/")             # The "@" decorator associates this route with the function
def hello_world():          
    return "Hello World!"

@app.route("/dojo")
def dojo():
    return "Dojo!"

@app.route("/say/<name>")
def say_my_name(name):
    return "Hello " + str(name) + "!"

@app.route("/repeat/<n>/<word>")
def repeat(n, word):
    return (str(word) + (" ")) * int(n)

@app.route("/<idk>")
def unknown(idk):
    return "Sorry! No response. Try again."

if __name__ == "__main__":  # Ensure this file is being run directly and not from a different module
    app.run(debug = True)   # Run the app in debug mode