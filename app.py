{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, render_template, redirect\n",
    "from flask_pymongo import PyMongo\n",
    "import scrape_mars\n",
    "\n",
    "# Create an instance of Flask\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Use PyMongo to establish Mongo connection\n",
    "mongo = PyMongo(app, uri=\"mongodb://localhost:27017/mars_app\")\n",
    "\n",
    "\n",
    "# Route to render index.html template using data from Mongo\n",
    "@app.route(\"/\")\n",
    "def home():\n",
    "\n",
    "    # Find one record of data from the mongo database\n",
    "    destination_data = mongo.db.mars_data.find_one()\n",
    "    # Return template and data\n",
    "    return render_template(\"index.html\", mission=destination_data)\n",
    "\n",
    "\n",
    "# Route that will trigger the scrape function\n",
    "@app.route(\"/scrape\")\n",
    "def scrape():\n",
    "\n",
    "    # Run the scrape function and save the results to a variable\n",
    "\n",
    "    news_results = scrape_mars.scrape_news_info()\n",
    "\n",
    "    featured_results = scrape_mars.scrape_featured_image()\n",
    "\n",
    "    weather_results = scrape_mars.scrape_weather_info()\n",
    "\n",
    "    facts_results = scrape_mars.scrape_mars_facts()\n",
    "\n",
    "    images_results = scrape_mars.scrape_full_res_images()\n",
    "\n",
    "    results = {\n",
    "        'news':news_results,\n",
    "        'featured_image': featured_results,\n",
    "        'weather':weather_results,\n",
    "        'facts': facts_results,\n",
    "        'hemispheres': images_results\n",
    "    }\n",
    "\n",
    "    # Update the Mongo database using update and upsert=True\n",
    "\n",
    "    mongo.db.mars_data.update({},results,upsert=True)\n",
    "    # Redirect back to home page\n",
    "    return redirect(\"/\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
