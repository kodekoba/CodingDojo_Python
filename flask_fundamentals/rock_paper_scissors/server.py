from flask import Flask, render_template, request, redirect
import random 
app = Flask(__name__)

# random.randrange(3)

@app.route('/')
def index():
    print(request)
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    print(request.form)
    form_pick = request.form['pick']

    rng = random.randint(1,3)
    if rng == 1:
        x = "Paper"
    if rng == 2:
        x = "Scissors"
    if rng == 3:
        x = "Rock"

    def rps(stg1, stg2):
        if (stg1 == "Rock" and stg2 == "Paper") or (stg1 == "Scissors" and stg2 == "Paper") or (stg1 == "Paper" and stg2 == "Rock"):
            return "You Win!"
        if (stg1 == "Rock" and stg2 =="Paper") or (stg1 == "Scissors" and stg2 == "Rock") or (stg1 == "Paper" and stg2 == "Scissors"):
            return "You Lose!"
        if (stg1 == "Rock" and stg2 =="Rock") or (stg1 == "Scissors" and stg2 == "Scissors") or (stg1 == "Paper" and stg2 == "Paper"):
            return "Tie"
    y =rps(request.form['pick'], x)
    return render_template("result.html", pick_template = form_pick, comp_template = x, output_template = y)

if __name__ =="__main__":
    app.run(debug=True)