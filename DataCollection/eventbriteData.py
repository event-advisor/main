# file to collect data from eventbrite
from requests import get
import os
from datetime import datetime

class EventbriteData:
    
    def __init__(self):
        # f = open(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\DataCollection\token.txt","r")
        # credentials = f.read()
        # f.close()
        # txt_arr = credentials.split("\n")
        # self._token = txt_arr[0]
        self._token = os.environ.get('event-token')
        self._url = "https://www.eventbriteapi.com/v3/events/search"
        self.category_dict = {"Arts": "Performing & Visual Arts", 
                     "Business": "Business & Professional",
                     "Charity": "Charity & Causes",
                     "Culture": "Community & Culture",
                     "Education": "Family & Education",
                     "Family": "Family & Education",             
                     "Fashion": "Fashion & Beauty",
                     "Film": "Film, Media & Entertainment",
                     "Food": "Food & Drink",
                     "Health": "Health & Wellness",
                     "Hobbies": "Hobbies & Special Interest",
                     "Music": "Music",
                     "Outdoors": "Travel & Outdoor",
                     "Religion": "Religion & Spirituality",
                     "Tech": "Science & Technology",
                     "Sports": "Sports & Fitness"}
        
        
    def getData(self,page,searchtxt):
        eventsearchtxt = self.category_dict.get(searchtxt)
        if (eventsearchtxt is not None):
            searchtxt = eventsearchtxt
        payload = {"q":searchtxt,
           "location.address":"singapore",
           "page":page,
           "sort_by": "date",
           "expand":"venue",
           "token":self._token}
        response = get(self._url,params=payload).json()["events"]
        return response
        
    def getEventName(self,items):
        names = []
        for i in range(len(items)):
            name = "[Eventbrite] " + items[i].get("name").get("text")
            names.append(name)
        return names
    def getEventUrl(self,items):
        urls = []
        for i in range(len(items)):
            url = items[i].get("url")
            urls.append(url)
        return urls

    def getEventlocation(self,items):
        eventLocations=[]
        for i in range(len(items)):
            eventLocation = items[i].get('venue').get('address')
            eventAddress = eventLocation.get('localized_address_display')
            eventLocations.append(eventAddress)
        return eventLocations

    def getEventTime(self,items):
        eventTimes=[]
        for i in range(len(items)):
             # Date & Start Time
            date_time = items[i].get("start")["local"].split("T")
            starttime = datetime.strptime(date_time[1],"%H:%M:%S")
            eventTimes.append(str(starttime.time()))
        return eventTimes

    def getEventDate(self,items):
        eventDates=[]
        for i in range(len(items)):
             # Date & Start Time
            date_time = items[i].get("start")["local"].split("T")
            date = datetime.strptime(date_time[0], "%Y-%m-%d")
            date = datetime.strftime(date,"%Y-%m-%d")
            eventDates.append(str(date))
        return eventDates