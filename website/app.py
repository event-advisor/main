from flask import Flask , flash, redirect, render_template, request, session, abort
import pandas as pd
import DataCollection.eventbriteData as eventbriteData

app = Flask(__name__)
eventData = eventbriteData.EventbriteData()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict/", methods =['GET'])
def predict():
    # user
    page = request.args.get("p",default = 1, type = str)
    searchtxt = request.args.get("q",default = 1, type = str)
    pageUrl = request.url

    #backend
    items = eventData.getData(page,searchtxt)
    eventNames = eventData.getEventName(items,searchtxt)
    eventUrls =  eventData.getEventUrl(items,searchtxt)
    eventImageUrls = eventData.getEventImageUrl(items,searchtxt)
    eventDescriptions = eventData.getEventDescription(items,searchtxt)
    eventLocations = eventData.getEventlocation(items,searchtxt)
    eventTimes = eventData.getEventTime(items,searchtxt)

    pageUrls= [ pageUrl[:-1] + str(i) for i in range(1,10)]

    return render_template("result.html",
    searchinput = searchtxt,
    eventNames = eventNames,
    eventUrls=eventUrls,
    eventImageUrls=eventImageUrls,
    eventDescriptions=eventDescriptions,
    eventLocations = eventLocations,
    eventTimes = eventTimes,
    pageUrls = pageUrls)

if __name__ == "__main__":
    app.run()