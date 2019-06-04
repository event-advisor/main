from flask import Flask , flash, redirect, render_template, request, session, abort
import DataCollection.eventbriteData as eventbriteData
import DataCollection.meetupData as meetupData
import DataCollection.peatixData as peatixDataInit
import time
import pandas as pd

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
    while (True):
        if (len(peatixItems) == 50):
            break
        items = peatixData.getData(peatixCounter,searchtxt)
        if (len(items) == 0):
            break
        peatixItems.extend(items)
        peatixCounter +=1
    peatixNames = peatixData.getEventName(peatixItems)
    peatixUrls =  peatixData.getEventUrl(peatixItems)
    peatixLocations = peatixData.getEventlocation(peatixItems)
    peatixTimes = peatixData.getEventTime(peatixItems)
    peatixDates = peatixData.getEventDate(peatixItems)
    print("peatix items:",len(peatixItems))
    print("peatix",time.time() - start)
    # eventbrite
    
    while (True):
        if (len(eventItems) == 50):
            break
        items = eventData.getData(eventCounter,searchtxt)
        if (len(items) == 0):
            break
        eventItems.extend(items)
        eventCounter +=1
    eventNames = eventData.getEventName(eventItems)
    eventUrls =  eventData.getEventUrl(eventItems)
    eventLocations = eventData.getEventlocation(eventItems)
    eventTimes = eventData.getEventTime(eventItems)
    eventDates = eventData.getEventDate(eventItems)
    print("event items:",len(eventItems))
    print("eventbrite",time.time() - start)
    # meetup 
    
    meetupNames = meetupData.getEventName(meetupItems)
    meetupUrls =  meetupData.getEventUrl(meetupItems)
    meetupLocations = meetupData.getEventlocation(meetupItems)
    meetupTimes = meetupData.getEventTime(meetupItems)
    meetupDates = meetupData.getEventDate(meetupItems)
    print("meetup items:",len(meetupItems))
    print("meetup",time.time() - start)

    # combining the items
    totalNames =list(map(str, peatixNames + eventNames + meetupNames))
    totalUrls = list(map(str,peatixUrls + eventUrls + meetupUrls))
    totalLocations = list(map(str, peatixLocations + eventLocations + meetupLocations))
    totalTimes = list(map(str, peatixTimes + eventTimes + meetupTimes))
    totalDates = list(map(str,peatixDates+eventDates + meetupDates))
    totalItems = pd.DataFrame(data={"Names":totalNames,"Urls":totalUrls,"Locations":totalLocations,"Times":totalTimes,"Dates":totalDates})
    totalItems = totalItems.sort_values(["Dates","Times"])

    # split into 15 items each
    totalNames15 = totalItems["Names"].tolist()[15*pages - 15: 15*pages]
    totalUrls15 = totalItems["Urls"].tolist()[15*pages - 15: 15*pages]
    totalLocations15 = totalItems["Locations"].tolist()[15*pages - 15: 15*pages]
    totalTimes15 = totalItems["Times"].tolist()[15*pages - 15: 15*pages]
    totalDates15 = totalItems["Dates"].tolist()[15*pages - 15: 15*pages]

    return render_template("meetup.html",
    searchinput = searchtxt,
    totalNames = totalNames15,
    totalUrls = totalUrls15,
    totalLocations = totalLocations15,
    totalTimes = totalTimes15,
    totalDates = totalDates15)

# @app.route("/shutdown")
# def shutdown():
#     peatixData._driver.close()
#     print("shutdown")
#     return render_template("index.html")

if __name__ == "__main__":
    myapp.run()