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

    category_dict = {"Arts": ["Performing & Visual Arts", "Arts"], 
                     "Business": ["Business & Professional", "Career & Business"],
                     "Charity": ["Charity & Causes", "Movements"],
                     "Culture": ["Community & Culture", "Language & Culture"],
                     "Education": ["Family & Education", "Learning"],
                     "Family": ["Family & Education", "Family"],             
                     "Fashion": ["Fashion & Beauty", "Fashion & Beauty"],
                     "Film": ["Film, Media & Entertainment", "Film"],
                     "Food": ["Food & Drink", "Food & Drink"],
                     "Health": ["Health & Wellness", "Health & Wellness"],
                     "Hobbies": ["Hobbies & Special Interest", "Hobbies & Crafts"],
                     "Music": ["Music", "Music"],
                     "Outdoors": ["Travel & Outdoor", "Outdoors & Adventure"],
                     "Religion": ["Religion & Spirituality", "Beliefs"],
                     "Tech": ["Science & Technology", "Tech"],
                     "Sports": ["Sports & Fitness", "Sports & Fitness"]}

    eb_category = category_dict[category][0]
    mu_category = category_dict[category][1]

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