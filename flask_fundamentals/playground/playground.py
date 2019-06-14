from flask import Flask, render_template
app = Flask(__name__)

@app.route("/play")
def index():
    return render_template("index.html", times = 3, color = "blue")

@app.route("/play/<x>")
def blue_boxes(x):
    return render_template("index.html", times = int(x), color = "blue")

@app.route("/play/<x>/<color>")
def colored_boxes(x, color):
    return render_template("index.html", times = int(x), color = color)

if __name__ == "__main__":
    app.run(debug = True) 