from requests import get
import os
class MeetUpData:
    
    def __init__(self):
        self._token = os.environ.get('event-token')
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
                   "access_token" : self._token,
                   "page": "50"}
        response = get(self._url,params=payload).json()["events"]
        return response
    def getEventName(self,items,searchtxt):
        names =[]
        for i in range(len(items)):
            name = items[i].get("name")
            names.append(name)
        return names
    def getEventUrl(self,items,searchtxt):
        urls = []
        for i in range(len(items)):
            url = items[i].get("link")
            urls.append(url)
        return urls
    def getEventlocation(self,items,searchtxt):
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
    def getEventTime(self,items,searchtxt):
        eventTimes=[]
        for i in range(len(items)):
            eventStart = items[i].get("local_date")+" " + items[i].get("local_time")
            eventTimes.append(eventStart)
        return eventTimes