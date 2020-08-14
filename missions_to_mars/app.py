from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_html_data = mongo.db.collection.find_one()
    print(mars_html_data)
    # Return template and data
    return render_template("index.html", space=mars_html_data)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    space_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, space_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)