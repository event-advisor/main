from flask import Flask , flash, redirect, render_template, request, session, abort
import pandas as pd
import DataCollection.eventbriteData as eventbriteData

app = Flask(__name__)
eventData = eventbriteData.EventbriteData()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods =['POST'])
def predict():
    searchtxt = request.form['search']

    items = eventData.getData(searchtxt)
    eventNames = eventData.getEventName(items,searchtxt)
    eventUrls =  eventData.getEventUrl(items,searchtxt)
    eventImageUrls = eventData.getEventImageUrl(items,searchtxt)
    eventDescriptions = eventData.getEventDescription(items,searchtxt)
    eventLocations = eventData.getEventlocation(items,searchtxt)
    eventTimes = eventData.getEventTime(items,searchtxt)

    return render_template("result.html",
    searchinput = searchtxt,
    eventNames = eventNames,
    eventUrls=eventUrls,
    eventImageUrls=eventImageUrls,
    eventDescriptions=eventDescriptions,
    eventLocations = eventLocations,
    eventTimes = eventTimes)

if __name__ == "__main__":
    app.run()