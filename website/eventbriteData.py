# file to collect data from eventbrite
from requests import get

class EventbriteData:
    
    def __init__(self):
        f = open(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\website\token.txt","r")
        credentials = f.read()
        f.close()
        txt_arr = credentials.split("\n")
        self._token = txt_arr[0]
        self._url = "https://www.eventbriteapi.com/v3/events/search"
        
        
    def getData(self,searchtxt):
        payload = {"q":searchtxt,
           "location.address":"singapore",
           "token":self._token}
        response = get(self._url,params=payload).json()
        return response
        
    def getEventName(self,items,searchtxt):
        name = items["events"][0]["name"]["text"]
        return name
    def getEventUrl(self,items,searchtxt):
        url = items["events"][0]["url"]
        return url
    def getEventImageUrl(self,items,searchtxt):
        imageUrl = items["events"][0]['logo']['original']['url']
        return imageUrl