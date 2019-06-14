from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe" #set a secret key for security purposes

# https://stackoverflow.com/questions/42671298/python-counter-add-and-subtract

@app.route("/")
def index():
    try:
        print("key exists!")
        session["count"] += 1
    except KeyError:
        print("keyerror occurred")
        session["count"] = 1
    return render_template("index.html")

@app.route("/destroy_session")
def destroy():
    session.clear()		
    # session.pop("keep it secret, keep it safe"?)		# I can't figure out how to call this correctly
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
