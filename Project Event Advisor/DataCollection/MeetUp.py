from requests import post, get
from datetime import datetime, timedelta
import json

class MeetUp:
  def __init__(self):
    self._token = "efc73c9cf05e124153013e67a7e4b3f1"

  def categories_list(self):
    params = {"token": self._token}
    response = get('https://api.meetup.com/find/topic_categories/', params = params)
    categories_data = response.json()

    # Categories
    topic_categories = {}
    for i in range(len(categories_data)):
        id_num = categories_data[i]["id"]
        cat_name = categories_data[i]["name"]
        topic_categories[cat_name] = id_num

    return(topic_categories)

  def collectData(self, category, topic_categories):
    params = {"order": "time", 
              "topic_category": "{}".format(topic_categories[category]), 
              "access_token": self._token}
    url = "https://api.meetup.com/find/upcoming_events"        
    upcoming_data = get(url, params = params).json()
    events = upcoming_data["events"]
    event_list = []
      
    #Name, Date, Start Time, Venue, URL
    for i in range(len(events)):
      event_info = []
      event = events[i]

      name = event["name"]
      date = event["local_date"]
      date_time = date + " " +event["local_time"]
      start_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M") # Start Time
      
      start_time = start_time.strftime("%H:%M")

      try:
          venue = event["venue"]["name"]
      except KeyError:
          venue = "-"
              
      url = event["link"]
      
      event_info.extend([name, date, start_time, venue, url])
      event_list.append(event_info)
      if len(event_list) == 50:
        break

    return(event_list)
