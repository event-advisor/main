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
peatixCounter = 1
eventCounter = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict/", methods =['POST'])
def predict():
    searchtxt = request.form['search']
    items = eventData.getData("1",searchtxt)
    # user
    page = "1"
    searchtxt = request.args.get("q",default = 1, type = str)

    #backend
    items = eventData.getData(page,searchtxt)
    eventNames = eventData.getEventName(items,searchtxt)
    eventUrls =  eventData.getEventUrl(items,searchtxt)
    # eventImageUrls = eventData.getEventImageUrl(items,searchtxt)
    # eventDescriptions = eventData.getEventDescription(items,searchtxt)
    # eventLocations = eventData.getEventlocation(items,searchtxt)
    # eventTimes = eventData.getEventTime(items,searchtxt)

    #pagination
    pageUrls= "[ pageUrl[:-1] + str(i) for i in range(1,10)]"

    return render_template("result.html",
    searchinput = searchtxt,
    eventNames = eventNames,
    eventUrls=eventUrls)
    # eventImageUrls=eventImageUrls,
    # eventDescriptions=eventDescriptions,
    # eventLocations = eventLocations,
    # eventTimes = eventTimes)

@app.route("/meetup/", methods =['GET'])
def meetup():
    global eventCounter
    global peatixCounter
    start = time.time()

    page = request.args.get("p",default = 1, type = str)
    searchtxt = request.args.get("search",default = 1, type = str)
    pages = int(page)
    print(page)

    print("--------------------------------")
    # peatix
    peatixItems = peatixData.getData(peatixCounter,searchtxt)
    peatixNames = peatixData.getEventName(peatixItems,searchtxt)[5*pages-5:5*pages]
    peatixUrls =  peatixData.getEventUrl(peatixItems,searchtxt)[5*pages-5:5*pages]
    peatixLocations = peatixData.getEventlocation(peatixItems,searchtxt)[5*pages-5:5*pages]
    peatixTimes = peatixData.getEventTime(peatixItems,searchtxt)[5*pages-5:5*pages]
    print(len(peatixItems))
    print("peatix",time.time() - start)
    # eventbrite
    eventItems = eventData.getData(eventCounter,searchtxt)
    eventNames = eventData.getEventName(eventItems,searchtxt)[5*pages-5:5*pages]
    if (eventNames == []):
        # if end of page
        eventCounter +=1
        eventItems = eventData.getData(eventCounter,searchtxt)
        eventNames = eventData.getEventName(eventItems,searchtxt)[5*pages-5:5*pages]
    eventUrls =  eventData.getEventUrl(eventItems,searchtxt)[5*pages-5:5*pages]
    eventLocations = eventData.getEventlocation(eventItems,searchtxt)[5*pages-5:5*pages]
    eventTimes = eventData.getEventTime(eventItems,searchtxt)[5*pages-5:5*pages]
    print("eventbrite",time.time() - start)
    # meetup 
    meetupItems = meetupData.getData(searchtxt)
    meetupNames = meetupData.getEventName(meetupItems,searchtxt)[:5*pages]
    meetupUrls =  meetupData.getEventUrl(meetupItems,searchtxt)[:5*pages]
    meetupLocations = meetupData.getEventlocation(meetupItems,searchtxt)[:5*pages]
    meetupTimes = meetupData.getEventTime(meetupItems,searchtxt)[:5*pages]
    print("meetup",time.time() - start)

    if (meetupItems == [] and eventItems == [] and peatixItems == []):
        return render_template("index.html")

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
    meetupTimes = meetupTimes)

@app.route("/shutdown")
def shutdown():
    peatixData._driver.close()
    print("shutdown")
    return render_template("index.html")

if __name__ == "__main__":
    app.run()