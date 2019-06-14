from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe"

@app.route("/")
def index():
    try:
        print("key exists!")
        # session["total_gold"] = session["total_gold"]
        yourgold = session["total_gold"]
    except KeyError:
        print("keyerror occurred")
        session["total_gold"] = 0
        yourgold = session["total_gold"]
    return render_template("index.html", totalgold = yourgold)

@app.route("/process_money", methods=["POST"])
def process_money():
    if request.form["building"] == "farm":
        session["total_gold"] += random.randint(10,20)
        return redirect("/")
    elif request.form["building"] == "cave":
        session["total_gold"] += random.randint(5,10)
        return redirect("/")
    elif request.form["building"] == "house":
        session["total_gold"] += random.randint(2,5)
        return redirect("/")
    elif request.form["building"] == "casino":
        session["total_gold"] += random.randint(-50,50)
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
