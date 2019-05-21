import requests
from datetime import datetime
import json

class Eventbrite:
    def __init__(self):
        f = open(r"/Users/student/Desktop/Project Event Advisor/Token.rtf", "r")
        credentials = f.read()
        f.close()
        txt_arr = credentials.split("\n")
        self._token = txt_arr[0]
        #self._token = "TOXBFSVPO5M67FQEFDOO"

    def categories_list(self):
        params = {"token": self._token}
        response = requests.get('https://www.eventbriteapi.com/v3/categories', params = params)
        categories_data = response.json()

        # Categories
        categories = {}
        for i in range(len(categories_data["categories"])):
            id_num = categories_data["categories"][i]["id"]
            cat_name = categories_data["categories"][i]["name"]
            categories[cat_name] = id_num

        return(categories)

    def collectData(self, category, categories):
        params = {"sort_by": "date", 
              "categories": "{}".format(categories[category]), 
              "location.address": "Singapore",
              "expand": "venue",
              "token": self._token}
              
        event_info_data = []
        page_number = 1

        while True:
            response = requests.get("https://www.eventbriteapi.com/v3/events/search/?page={}".format(page_number), params=params)
            upcoming_data = response.json()
            events = upcoming_data["events"]
            for i in range(len(events)):
                event_info = []
                event = events[i]
                
                # Date & Start Time
                date_time = event["start"]["local"].split("T")
                date = datetime.strptime(date_time[0], "%Y-%m-%d")
                date = datetime.strftime(date,"%Y-%m-%d")
                starttime = datetime.strptime(date_time[1],"%H:%M:%S")
                
                # Venue
                venue = event["venue"]["address"]["localized_address_display"]
                
                # Event Info (Name, Date, Start Time, Venue, Event URL)
                event_info.extend([event["name"]["text"], date, starttime.time().isoformat(), venue, event["url"]])
                if len(event_info)>0:
                    event_info_data.append(event_info)   
                if len(event_info_data)==50:
                    break

            if (len(event_info_data) == 50) or (upcoming_data["pagination"]["page_number"] == upcoming_data["pagination"]["page_count"]):
                break
            else:
                page_number += 1
      
        return(event_info_data)
