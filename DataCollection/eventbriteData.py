# file to collect data from eventbrite
from requests import get
import os

class EventbriteData:
    
    def __init__(self):
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
           "expand":"venue",
           "token":self._token}
        response = get(self._url,params=payload).json()["events"]
        return response
        
    def getEventName(self,items):
        names = []
        for i in range(len(items)):
            name = items[i].get("name").get("text")
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
            eventStart = "timezone : {} \n".format(items[i].get('start').get('timezone')) + items[i]['start']['local']
            eventTimes.append(eventStart)
        return eventTimes