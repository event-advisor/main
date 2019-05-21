from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

from requests import get

class Peatix:
  def __init__(self):
    self._url = "https://peatix.com/search"

  def collectData(self, category):
    result = []
    page = 1

    options = Options()
    options.add_argument("--headless")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.image", 2)
    driver = webdriver.Firefox(executable_path = "/Users/student/Downloads/geckodriver", options = options, firefox_profile=profile)
    while True:
      params = {"q": "{}".format(category),
                "country": "SG", 
                "p": "{}".format(page)}
      url = self._url      
      
      response = get(url,params=params)
      driver.get(response.url)

      html_soup = BeautifulSoup(driver.page_source, "html.parser")
      event_source = html_soup.find("div", attrs = {"class": "event-search-results col-main"})
      event_containers = event_source.find_all("a", attrs = {"class": "event-thumb_link"})    
      if len(event_containers) == 0:
        driver.close()
        break
      else:
        main_event_list=[]
        for event in event_containers:
          event_list = []
          # Name, Date, Start Time, Venue, Event URL
          name = event.h3.text

          venue = event.find_all("span")[2].text[3:]

          url = str(event).split("href=\"")[1].split("\" ")[0]

          date = str(event.find_all("time")[0]).split(" ")[2].split("=\"")[1]
          
          start_time = str(event.find_all("time")[0]).split(" ")[3]
          date_time = date + " " + start_time
          start_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
          start_time = start_time.strftime("%H:%M:%S")
          
          event_list.extend([name,date,start_time,venue,url])
          main_event_list.append(event_list)

      result.extend(main_event_list)
      if len(result) == 50:
        return(result)
      else:
        page += 1  


    return(result)
