from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
@app.route("/")
def index():
    mars = mongo.db.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

