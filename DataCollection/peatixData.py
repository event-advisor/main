from requests import get
from selenium import webdriver 
from bs4 import BeautifulSoup

class peatixData:
    
    def __init__(self):
        self.CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
        self._url = "https://peatix.com/search"
        options = webdriver.ChromeOptions()
        options.binary_location = '.apt/usr/bin/google-chrome-stable'
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        options.add_experimental_option("prefs",prefs)
        self._driver = webdriver.Chrome(self.CHROMEDRIVER_PATH,options = options)
        
    def getDataUrl(self,page,searchtxt):
        mode =""
        payload = { "q":searchtxt,
                "country":"SG",
                "l.ll":"1.3553794,103.86774439999999",
                "l.text":"Singapore",
                "p":page,
                "size":"10",
                "v":"3.4",
                "dr":mode
        }
        theUrl = get(self._url,params=payload).url
        return theUrl

    def getData(self,page,searchtxt):
        theUrl = self.getDataUrl(page,searchtxt)
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
        return list(map(str,names))
    def getEventUrl(self,items,searchtxt):
        urls = []
        for i in range(len(items)):
            url = items[i].a["href"]
            urls.append(url)
        return list(map(str,urls))

    def getEventlocation(self,items,searchtxt):
        eventLocations=[]
        for i in range(len(items)):
            eventAddress = items[i].find("span",class_ ="event-thumb_location ng-binding").text
            eventLocations.append(eventAddress)
        f = lambda  x: "None" if x == None else x
        return list(map(f,eventLocations))

    def getEventTime(self,items,searchtxt):
        eventTimes=[]
        for i in range(len(items)):
            eventTime = items[i].time["datetime"]
            eventTimes.append(eventTime)
        return list(map(str,eventTimes))