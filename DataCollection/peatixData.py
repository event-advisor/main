from requests import get
from selenium import webdriver 
from bs4 import BeautifulSoup
import time
from datetime import datetime
class peatixData:
    
    def __init__(self):
        self.CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
        self._url = "https://peatix.com/search"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        options.add_experimental_option("prefs",prefs)
        options.binary_location = '/app/.apt/usr/bin/google-chrome'
        self.driver = webdriver.Chrome(self.CHROMEDRIVER_PATH,options = options)
        # self.driver = webdriver.Chrome(r"C:\Users\wen kai\Downloads\y4s2\event-advisor\DataCollection\chromedriver.exe",options = options)
        

        
        
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
        self.driver.get(theUrl)
        time.sleep(0.6)
        html_soup = BeautifulSoup(self.driver.page_source,'html.parser')
        event_containers = html_soup.find_all("li",class_="event-thumb ng-scope")
        return event_containers

    def getEventName(self,items):
        names =[]
        for i in range(len(items)):
            event_details = items[i].find("div",class_="event-thumb_detail")
            name =  "Peatix " +event_details.h3.text
            names.append(name)
        return names
    def getEventUrl(self,items):
        urls = []
        for i in range(len(items)):
            url = items[i].a["href"]
            urls.append(url)
        return urls

    def getEventlocation(self,items):
        eventLocations=[]
        for i in range(len(items)):
            eventAddress = items[i].find("span",class_ ="event-thumb_location ng-binding").text
            eventLocations.append(eventAddress)
        return eventLocations

    def getEventDate(self,items):
        eventDates=[]
        for i in range(len(items)):
            event_date_time = items[i].time["datetime"].split(" ")
            eventDate = event_date_time[0]
            eventDates.append(eventDate)
        return eventDates
    
    def getEventTime(self,items):
        eventTimes=[]
        for i in range(len(items)):
            event_date_time = items[i].time["datetime"].split(" ")
            eventTime = event_date_time[1]
            eventDate = event_date_time[0]
            date_time = eventDate + " " + eventTime
            start_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            start_time = start_time.strftime("%H:%M:%S")
            eventTimes.append(start_time)
        return eventTimes