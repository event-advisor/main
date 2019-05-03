from flask import Flask , flash, redirect, render_template, request, session, abort
import pandas as pd
import DataCollection.eventbriteData as eventbriteData
import DataCollection.meetupData as meetupData
import DataCollection.peatixData as peatixDataInit
import time

app = Flask(__name__)
eventData = eventbriteData.EventbriteData()
meetupData = meetupData.MeetUpData()
peatixData = peatixDataInit.peatixData()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods =['POST'])
def predict():
    searchtxt = request.form['search']
    items = eventData.getData(searchtxt)
    eventNames = eventData.getEventName(items,searchtxt)
    eventUrls =  eventData.getEventUrl(items,searchtxt)
    # eventImageUrls = eventData.getEventImageUrl(items,searchtxt)
    # eventDescriptions = eventData.getEventDescription(items,searchtxt)
    # eventLocations = eventData.getEventlocation(items,searchtxt)
    # eventTimes = eventData.getEventTime(items,searchtxt)

    return render_template("result.html",
    searchinput = searchtxt,
    eventNames = eventNames,
    eventUrls=eventUrls)
    # eventImageUrls=eventImageUrls,
    # eventDescriptions=eventDescriptions,
    # eventLocations = eventLocations,
    # eventTimes = eventTimes)

@app.route("/meetup", methods =['POST'])
def meetup():
    start = time.time()
    searchtxt = request.form['search']
    if (searchtxt == ""):
        category_arr ={"tech":"Technology","cook":"cooking"}
        searchtxt = request.form['category']
        searchtxt = category_arr[searchtxt]
    
    print(time.time() - start)
    # peatix
    peatixItems = peatixData.getData(searchtxt)
    peatixNames = peatixData.getEventName(peatixItems,searchtxt)
    peatixUrls =  peatixData.getEventUrl(peatixItems,searchtxt)
    peatixLocations = peatixData.getEventlocation(peatixItems,searchtxt)
    peatixTimes = peatixData.getEventTime(peatixItems,searchtxt)
    print("peatix",time.time() - start)
    # eventbrite
    eventItems = eventData.getData(searchtxt)
    eventNames = eventData.getEventName(eventItems,searchtxt)
    eventUrls =  eventData.getEventUrl(eventItems,searchtxt)
    eventLocations = eventData.getEventlocation(eventItems,searchtxt)
    eventTimes = eventData.getEventTime(eventItems,searchtxt)
    print("eventbrite",time.time() - start)
    # meetup 
    meetupItems = meetupData.getData(searchtxt)
    meetupNames = meetupData.getEventName(meetupItems,searchtxt)
    meetupUrls =  meetupData.getEventUrl(meetupItems,searchtxt)
    meetupLocations = meetupData.getEventlocation(meetupItems,searchtxt)
    meetupTimes = meetupData.getEventTime(meetupItems,searchtxt)
    print("meetup",time.time() - start)

    return render_template("meetup.html",
    searchinput = searchtxt,
    peatixNames = peatixNames,
    peatixUrls = peatixUrls,
    peatixLocations = peatixLocations,
    peatixTimes = peatixTimes,
    eventNames = eventNames,
    eventUrls = eventUrls,
    eventLocations = eventLocations,
    eventTimes = eventTimes,
    meetupNames = meetupNames,
    meetupUrls= meetupUrls,
    meetupLocations = meetupLocations,
    meetupTimes = meetupTimes
    )

@app.route("/shutdown")
def shutdown():
    peatixData._driver.close()
    print("shutdown")
    return render_template("index.html")

if __name__ == "__main__":
    app.run()