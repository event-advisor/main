from requests import get

class MeetUpData:
    
    def __init__(self):
        f = open(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\website\DataCollection\token.txt","r")
        credentials = f.read()
        f.close()
        txt_arr = credentials.split("\n")
        self._token = txt_arr[1]
        self._url = "https://api.meetup.com/find/upcoming_events/"
        
        
    def getData(self,searchtxt):
        payload = { "text":searchtxt,
                   "access_token" : self._token,
                   "page": "11"}
        response = get(self._url,params=payload).json()["events"]
        return response
    def getEventName(self,items,searchtxt):
        names =[]
        for i in range(len(items)):
            if ( i == 10):
                break
            name = items[i]["name"]
            names.append(name)
        return names
    def getEventUrl(self,items,searchtxt):
        urls = []
        for i in range(len(items)):
            if ( i == 10):
                break
            url = items[i]["link"]
            urls.append(url)
        return urls
    def getEventlocation(self,items,searchtxt):
        eventLocations=[]
        for i in range(5):
            eventLocation = items[i]['venue']['name']
            eventLocationAddress = items[i]['venue']['address_1']
            eventAddress = eventLocation + " " + eventLocationAddress 
            eventLocations.append(eventAddress)
        return eventLocations
    def getEventTime(self,items,searchtxt):
        eventTimes=[]
        for i in range(len(items)):
            eventStart = items[i]["local_date"]+" " + items[i]["local_time"]
            eventEnd = str(int(items[i]["duration"])/(60*1000)) + "minutes"
            eventTime = [eventStart,eventEnd]
            eventTimes.append(eventTime)
        return eventTimes