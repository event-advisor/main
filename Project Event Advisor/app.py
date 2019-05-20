from flask import Flask, flash, redirect, render_template, request, session, abort

import requests
import json
from datetime import datetime
import pandas as pd
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Load API for Categories
def categories_list():
    headers = {'Authorization': 'Bearer TOXBFSVPO5M67FQEFDOO'}
    response = requests.get('https://www.eventbriteapi.com/v3/categories', headers=headers)
    data = response.text
    categories_data = json.loads(data)

    # Categories
    categories = {}
    for i in range(len(categories_data["categories"])):
        id_num = categories_data["categories"][i]["id"]
        cat_name = categories_data["categories"][i]["name"]
        categories[cat_name] = id_num

    return(categories)
    

def load_api(category, categories):
    params = {"sort_by": "date", 
            "categories": "{}".format(categories[category]), 
            "location.address": "Singapore"}
    headers = {'Authorization': 'Bearer TOXBFSVPO5M67FQEFDOO'}
    event_info_data = []
    page_number = 1

    while True:
        response = requests.get("https://www.eventbriteapi.com/v3/events/search/?page={}".format(page_number), headers=headers,params=params)
        data = response.text
        data = json.loads(data)
        events = data["events"]
        for i in range(len(events)):
            event_info = []
            event = events[i]
            # Duration of Event
            duration = (datetime.strptime(event["end"]["local"],"%Y-%m-%dT%H:%M:%S")- datetime.strptime(event["start"]["local"],"%Y-%m-%dT%H:%M:%S")).seconds/3600
            # Description of Event (First 50 Words)
            description = " ".join(event["description"]["text"].split(" ")[:51])
            # Event Logo
            if event["logo"] != None:
                image_url = event["logo"]["url"]
            else:
                image_url = "-"

            # Event Info (Name, Start Time, End Time, Duration, Free, Description, Image URL, Event URL)
            event_info.extend([event["name"]["text"], event["start"]["local"].replace("T"," "), event["end"]["local"].replace("T"," "), duration, event["is_free"], description, image_url, event["url"]])
            if len(event_info)>0:
                event_info_data.append(event_info)   

        if data["pagination"]["page_number"] == data["pagination"]["page_count"]:
            break
        else:
            page_number += 1
    
    return(event_info_data)

@app.route("/retrieve", methods = ["POST"])
def retrieve():
    category = request.form["category"]
    if category == "Business":
        category = "Business & Professional"
    elif category == "Science & Tech":
        category = "Science & Technology"
    elif category == "Film & Media":
        category = "Film, Media & Entertainment"
    elif category == "Arts":
        category = "Performing & Visual Arts"
    elif category == "Fashion":
        category = "Fashion & Beauty"
    elif category == "Health":
        category = "Health & Wellness"
    elif category == "Government":
        category = "Government & Politics"
    elif category == "Community":
        category = "Community & Culture"
    elif category == "Spirituality":
        category = "Religion & Spirituality"
    elif category == "Holiday":
        category = "Seasonal & Holiday"
    elif category == "Hobbies":
        category = "Hobbies & Special Interest"
    
    x = load_api(category, categories_list())
    return render_template('result.html', listing = x)

if __name__ == "__main__":
    app.run()