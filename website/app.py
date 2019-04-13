from flask import Flask , flash, redirect, render_template, request, session, abort
import pandas as pd
import eventbriteData as eventbriteData

app = Flask(__name__)
eventData = eventbriteData.EventbriteData()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods =['POST'])
def predict():
    searchtxt = request.form['search']

    items = eventData.getData(searchtxt)
    eventName = eventData.getEventName(items,searchtxt)
    eventUrl =  eventData.getEventUrl(items,searchtxt)
    eventImageUrl = eventData.getEventImageUrl(items,searchtxt)

    return render_template("result.html",searchinput = searchtxt,
    eventName = eventName,eventUrl=eventUrl,eventImageUrl=eventImageUrl)

if __name__ == "__main__":
    app.run()