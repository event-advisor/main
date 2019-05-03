from requests import get
from selenium import webdriver
from bs4 import BeautifulSoup

class peatixData:
    
    def __init__(self):
        self._url = "https://peatix.com/search"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        options.add_experimental_option("prefs",prefs)
        self._driver = webdriver.Chrome(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\website\DataCollection\chromedriver.exe",options = options)
        
    def getDataUrl(self,searchtxt):
        mode =""
        payload = { "q":searchtxt,
                "country":"SG",
                "l.ll":"1.3553794,103.86774439999999",
                "l.text":"Singapore",
                "p":"1",
                "size":"10",
                "v":"3.4",
                "dr":mode
        }
        theUrl = get(self._url,params=payload).url
        return theUrl

    def getData(self,searchtxt):
        theUrl = self.getDataUrl(searchtxt)
        self._driver.get(theUrl)
        html_soup = BeautifulSoup(self._driver.page_source,'html.parser')
        event_containers = html_soup.find_all("li",class_="event-thumb ng-scope")
        return event_containers

    def getEventName(self,items,searchtxt):
        names =[]
        for i in range(len(items)):
            event_details = items[i].find("div",class_="event-thumb_detail")
            name =  event_details.h3.text
            names.append(name)
        return names
    def getEventUrl(self,items,searchtxt):
        urls = []
        for i in range(len(items)):
            url = items[i].a["href"]
            urls.append(url)
        return urls

    def getEventlocation(self,items,searchtxt):
        eventLocations=[]
        for i in range(len(items)):
            eventAddress = items[i].find("span",class_ ="event-thumb_location ng-binding").text
            eventLocations.append(eventAddress)
        return eventLocations

    def getEventTime(self,items,searchtxt):
        eventTimes=[]
        for i in range(len(items)):
            eventStart = items[i].time["datetime"]
            eventEnd = items[i].time["datetime"] 
            eventTime = [eventStart,eventEnd]
            eventTimes.append(eventTime)
        return eventTimes