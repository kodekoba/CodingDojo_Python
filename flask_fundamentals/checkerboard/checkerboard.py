from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", columns = 8, rows = 8, color1 = "green", color2 = "black")

@app.route("/<n>")
def alt(n):
    return render_template("index.html", columns = 8, rows = int(n))

# @app.route("/<n>/<color1>/<color2>")
# def alt(n):
#     return render_template("index.html", columns = 8, rows = int(n))

if __name__ == "__main__":
    app.run(debug = True) 