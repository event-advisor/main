from flask import Flask , flash, redirect, render_template, request, session, abort
import pandas as pd
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods =['POST'])
def predict():
    searchtxt = request.form['search']
    return render_template("result.html",searchinput = searchtxt)

if __name__ == "__main__":
    app.run()