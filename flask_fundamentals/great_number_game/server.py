from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe"

@app.route("/")
def index():
    # if x != session["rnum"]:
        session["rnum"] = random.randint(1,100)
        # x = session["rnum"]
        # print(x)
        print(session["rnum"])
        return render_template("index.html")
    # else: return render_template("index.html")

@app.route("/guess", methods=["POST"])
def guess():
    if int(request.form["guess"]) == session["rnum"]:
        response = "That was the number!"
        return render_template("index.html", goodresponse = response)
    elif int(request.form["guess"]) > session["rnum"]:
        response = "That's too high!"
        return render_template("index.html", badresponse = response)
    else:
        response = "That's too low!"
        return render_template("index.html", badresponse = response)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
