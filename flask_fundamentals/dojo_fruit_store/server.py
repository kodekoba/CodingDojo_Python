from flask import Flask, render_template, request, redirect
app = Flask(__name__)  

@app.route('/')         
def index():
    return render_template("index.html")

@app.route('/checkout', methods=['POST'])         
def checkout():     # reloading the page means we get charged again :(
    print(request.form)
    sb_from_form = int(request.form["strawberry"])
    rb_from_form = int(request.form["raspberry"])
    ap_from_form = int(request.form["apple"])
    fn_from_form = request.form["first_name"]
    ln_from_form = request.form["last_name"]
    id_from_form = request.form["student_id"]
    count = int(sb_from_form + rb_from_form + ap_from_form)
    print("Charging " + request.form["first_name"] + " " + request.form["last_name"] + " for " + str(count) + " fruits")
    return render_template("checkout.html", sb = sb_from_form, rb = rb_from_form, ap = ap_from_form, fn = fn_from_form, ln = ln_from_form, id = id_from_form)
    

@app.route('/fruits')         
def fruits():
    return render_template("fruits.html")

if __name__=="__main__":   
    app.run(debug=True)    