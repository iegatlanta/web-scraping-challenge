from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time as tm

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# creating route to find HTML page

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# scraping route
@app.route("/scrape_mars")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)   
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()
