from requests import get
from datetime import datetime
import os
class MeetUpData:
    
    def __init__(self):
        # f = open(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\DataCollection\token.txt","r")
        # credentials = f.read()
        # f.close()
        # txt_arr = credentials.split("\n")
        # self._token = txt_arr[1]
        self._token = os.environ.get('meetup-token')
        self._url = "https://api.meetup.com/find/upcoming_events/"
        self.category_dict = {"Arts": "Arts", 
                     "Business":  "Career & Business",
                     "Charity":  "Movements",
                     "Culture":  "Language & Culture",
                     "Education": "Learning",
                     "Family": "Family",             
                     "Fashion": "Fashion & Beauty",
                     "Film":  "Film",
                     "Food":  "Food & Drink",
                     "Health":  "Health & Wellness",
                     "Hobbies":  "Hobbies & Crafts",
                     "Music": "Music",
                     "Outdoors": "Outdoors & Adventure",
                     "Religion": "Beliefs",
                     "Tech":  "Tech",
                     "Sports": "Sports & Fitness"}
        
    def getData(self,searchtxt):
        meetupsearchtxt = self.category_dict.get(searchtxt)
        if (meetupsearchtxt is not None):
            searchtxt = meetupsearchtxt
        payload = { "text":searchtxt,
                    "order": "time",
                   "access_token" : self._token,
                   "page": "50"}
        response = get(self._url,params=payload).json().get("events")
        return response
    def getEventName(self,items):
        names =[]
        for i in range(len(items)):
            name = "Meetup " + items[i].get("name")
            names.append(name)
        return names
    def getEventUrl(self,items):
        urls = []
        for i in range(len(items)):
            url = items[i].get("link")
            urls.append(url)
        return urls
    def getEventlocation(self,items):
        eventLocations=[]
        for i in range(len(items)):
            if ( items[i].get('venue') is not None):
                eventLocation = items[i].get('venue').get('name')
                eventLocationAddress = items[i].get('venue').get('address_1')
                eventAddress = str(eventLocation) + " " + str(eventLocationAddress)
                eventLocations.append(eventAddress)
            else:
                eventLocations.append("None")
        return eventLocations
    def getEventTime(self,items):
        eventTimes=[]
        for i in range(len(items)):
            date =  items[i].get("local_date")
            date_time = date + " " +items[i].get("local_time")
            start_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M") # Start Time
            start_time = start_time.strftime("%H:%M")+":00"
            eventTimes.append(start_time)
        return eventTimes

    def getEventDate(self,items):
        eventDates=[]
        for i in range(len(items)):
            eventStart = items[i].get("local_date")
            eventDates.append(eventStart)
        return eventDates