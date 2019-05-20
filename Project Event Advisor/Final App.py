from flask import Flask, flash, redirect, render_template, request, session, abort
import DataCollection.EventBrite as EventBrite
import DataCollection.MeetUp as MeetUp
import DataCollection.Peatix as Peatix


app = Flask(__name__)
EventBrite = EventBrite.Eventbrite()
MeetUp = MeetUp.MeetUp()
Peatix = Peatix.Peatix()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/retrieve", methods = ["POST"])
def retrieve():
    category = request.form["category"]
    if category == "Arts":
        eb_category = "Performing & Visual Arts"
        mu_category = "Arts"
    elif category == "Business":
        eb_category = "Business & Professional"
        mu_category = "Career & Business"
    elif category == "Charity":
        eb_category = "Charity & Causes"
        mu_category = "Movements"
    elif category == "Culture":
        eb_category = "Community & Culture"
        mu_category = "Language & Culture"
    elif category == "Education":
        eb_category = "Family & Education"
        mu_category = "Learning"
    elif category == "Family":
        eb_category = "Family & Education"
        mu_category = "Family"
    elif category == "Fashion":
        eb_category = "Fashion & Beauty"
        mu_category = "Fashion & Beauty"
    elif category == "Film":
        eb_category = "Film, Media & Entertainment"
        mu_category = "Film"
    elif category == "Food":
        eb_category = "Food & Drink"
        mu_category = "Food & Drink"
    elif category == "Health":
        eb_category = "Health & Wellness"
        mu_category = "Health & Wellness"
    elif category == "Hobbies":
        eb_category = "Hobbies & Special Interest"
        mu_category = "Hobbies & Crafts"
    elif category == "Music":
        eb_category = "Music"
        mu_category = "Music"
    elif category == "Outdoors":
        eb_category = "Travel & Outdoor"
        mu_category = "Outdoors & Adventure"
    elif category == "Religion":
        eb_category = "Religion & Spirituality"
        mu_category = "Beliefs"
    elif category == "Science & Tech":
        eb_category = "Science & Technology"
        mu_category = "Tech"
    elif category == "Sports":
        eb_category = "Sports & Fitness"
        mu_category = "Sports & Fitness"

    eb_categories = EventBrite.categories_list()
    mu_categories = MeetUp.categories_list()
    
    eb_results = EventBrite.collectData(eb_category, eb_categories)  
    mu_results = MeetUp.collectData(mu_category, mu_categories)
    p_results = Peatix.collectData(category)  

    final_results = []
    for i in [eb_results,mu_results,p_results]:
        final_results.extend(i)
    final_results.sort(key = lambda x: (x[1],x[2]))
    return render_template('result.html', final_results = final_results)

if __name__ == "__main__":
    app.run()