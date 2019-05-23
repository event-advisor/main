from flask import Flask , flash, redirect, render_template, request, session, abort
import DataCollection.eventbriteData as eventbriteData
import DataCollection.meetupData as meetupData
import DataCollection.peatixData as peatixDataInit
import time

myapp = Flask(__name__)
eventData = eventbriteData.EventbriteData()
meetupData = meetupData.MeetUpData()
peatixData = peatixDataInit.peatixData()
eventItems = []
peatixItems = []
meetupItems = []
searchtxt = ""




@myapp.route("/")
def index():
    return render_template("index.html")

@myapp.route("/meetup/", methods =['GET'])
def meetup():
    global peatixItems
    global eventItems
    global meetupItems
    global searchtxt

    peatixCounter = 1
    eventCounter = 1
    start = time.time()

    page = request.args.get("p",default = 1, type = str)
    searchinput = request.args.get("search",default = 1, type = str)
    pages = int(page)
    
    if (searchtxt != searchinput):
        searchtxt = searchinput
        peatixItems = []
        eventItems = []
        meetupItems = meetupData.getData(searchtxt)
        print("new search term")
    print("--------------------------------")
    # peatix
    
    print(len(meetupItems))
    while (len(peatixItems) < 50):
        items = peatixData.getData(peatixCounter,searchtxt)
        if(items == []):
            break
        peatixItems.extend(items)
        peatixCounter +=1
    peatixNames = peatixData.getEventName(peatixItems,searchtxt)[5*pages-5:5*pages]
    peatixUrls =  peatixData.getEventUrl(peatixItems,searchtxt)[5*pages-5:5*pages]
    peatixLocations = peatixData.getEventlocation(peatixItems,searchtxt)[5*pages-5:5*pages]
    peatixTimes = peatixData.getEventTime(peatixItems,searchtxt)[5*pages-5:5*pages]
    print("peatix items:",len(peatixItems))
    print("peatix",time.time() - start)
    # eventbrite
    
    while (len(eventItems) < 50):
        eventCounter +=1
        items = eventData.getData(eventCounter,searchtxt)
        if ( items == []):
            break
        eventItems.extend(items)
    eventNames = eventData.getEventName(eventItems)[5*pages-5:5*pages]
    eventUrls =  eventData.getEventUrl(eventItems)[5*pages-5:5*pages]
    eventLocations = eventData.getEventlocation(eventItems)[5*pages-5:5*pages]
    eventTimes = eventData.getEventTime(eventItems)[5*pages-5:5*pages]
    print("event items:",len(eventItems))
    print("eventbrite",time.time() - start)
    # meetup 
    
    meetupNames = meetupData.getEventName(meetupItems,searchtxt)[5*pages-5:5*pages]
    meetupUrls =  meetupData.getEventUrl(meetupItems,searchtxt)[5*pages-5:5*pages]
    meetupLocations = meetupData.getEventlocation(meetupItems,searchtxt)[5*pages-5:5*pages]
    meetupTimes = meetupData.getEventTime(meetupItems,searchtxt)[5*pages-5:5*pages]
    print("meetup items:",len(meetupItems))
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

# @app.route("/shutdown")
# def shutdown():
#     peatixData._driver.close()
#     print("shutdown")
#     return render_template("index.html")

if __name__ == "__main__":
    myapp.run()