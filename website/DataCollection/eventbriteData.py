# file to collect data from eventbrite
from requests import get

class EventbriteData:
    
    def __init__(self):
        f = open(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\website\DataCollection\token.txt","r")
        credentials = f.read()
        f.close()
        txt_arr = credentials.split("\n")
        self._token = txt_arr[0]
        self._url = "https://www.eventbriteapi.com/v3/events/search"
        
        
    def getData(self,searchtxt):
        payload = {"q":searchtxt,
           "location.address":"singapore",
           "expand":"venue",
           "token":self._token}
        response = get(self._url,params=payload).json()["events"]
        return response
        
    def getEventName(self,items,searchtxt):
        names = []
        for i in range(10):
            name = items[i]["name"]["text"]
            names.append(name)
        return names
    def getEventUrl(self,items,searchtxt):
        urls = []
        for i in range(10):
            url = items[i]["url"]
            urls.append(url)
        return urls
    def getEventImageUrl(self,items,searchtxt):
        imageUrls=[]
        for i in range(10):
            logo = items[i]['logo']
            if (logo is None):
                imageUrls.append(items[0]['logo']['url'])
            else:
                imageUrl = logo['url']
                imageUrls.append(imageUrl)
        return imageUrls

    def getEventDescription(self,items,searchtxt):
        eventDescriptions=[]
        for i in range(10):
            eventDescription = items[i]['summary']
            eventDescriptions.append(eventDescription)
        return eventDescriptions  

    def getEventlocation(self,items,searchtxt):
        eventLocations=[]
        for i in range(10):
            eventLocation = items[i]['venue']['address']
            eventAddress = eventLocation['localized_address_display']
            eventLocations.append(eventAddress)
        return eventLocations

    def getEventTime(self,items,searchtxt):
        eventTimes=[]
        for i in range(10):
            eventStart = "timezone : {} \n".format(items[i]['start']['timezone']) + items[i]['start']['local']
            eventEnd = "timezone : {} \n".format(items[i]['end']['timezone']) + items[i]['end']['local']    
            eventTime = [eventStart,eventEnd]
            eventTimes.append(eventTime)
        return eventTimes