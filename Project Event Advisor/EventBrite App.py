from flask import Flask, flash, redirect, render_template, request, session, abort
import DataCollection.EventBrite as EventBrite

app = Flask(__name__)
EventBrite = EventBrite.Eventbrite()

@app.route("/")
def index():
    return render_template("index.html")

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

  categories = EventBrite.categories_list()
  results = EventBrite.collectData(category, categories)  
    
  return render_template('result.html', listing = results)

if __name__ == "__main__":
    app.run()