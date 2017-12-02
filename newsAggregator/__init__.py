import feedparser
import re
from flask import Flask, render_template
import string
import json
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from engine import *

app = Flask(__name__)
cnn_worldnews = feedparser.parse('http://rss.cnn.com/rss/cnn_world.rss')

app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class all_countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(2000))
    def __init__ (self, country):
        self.country = country

class news_urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(50))
    countries = db.Column(db.String(50))
    def __init__(self, url, countries):
        self.countries = countries
        self.url = url

def loop_through_news(news):
    file = open('data_lists/country-keyword-list.csv', encoding = 'UTF-16')
    country_dict = {}

    for line in file:
        data = json.loads(line)
        country_dict.update(data)
    i = 0

    while i < len(news.entries):
        s = (re.sub("<.*?>|\b's\b|", "", news.entries[i].summary))
        s = s.translate(str.maketrans('', '', string.punctuation))

        lists = s.split(" ")
        string_dictionary = dict.fromkeys(lists)

        for key, value in country_dict.items():
            for item in value:
                if item in string_dictionary:
                    if news.entries[i].title == "":
                        print (key + "  {{{"+ news.entries[i].link+ "}}}")
                        break
                    else:
                        print(key + "  {{{"+ news.entries[i].link + "}}}")
                        break
        i += 1

loop_through_news(cnn_worldnews)

@app.route("/")
def main():
    db.create_all()
    return render_template('index.html')

def sql_test():
    test = all_countries(country="gzdf")
    testy = news_urls(url="fda", countries="Dsa")
    db.session.add(testy)
    db.session.add(test)
    db.session.flush()
    db.session.commit()


sql_test()

if __name__ == "__main__":
    app.run()
