from flask import Flask, flash, redirect, render_template, request, session, abort
import DataCollection.MeetUp as MeetUp

app = Flask(__name__)
MeetUp = MeetUp.MeetUp()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/retrieve", methods = ["POST"])
def retrieve():
  category = request.form["category"]
  if category == "Business":
    category = "Career & Business"
  elif category == "Fashion":
    category = "Fashion & Beauty"
  elif category == "Health":
    category = "Health & Wellness"
  elif category == "Hobbies":
    category = "Hobbies & Crafts"

  categories = MeetUp.categories_list()
  results = MeetUp.collectData(category, categories)  
    
  return render_template('meetup_result.html', listing = results)

if __name__ == "__main__":
    app.run()