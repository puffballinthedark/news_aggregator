import feedparser
import re
from flask import Flask, render_template

import string
import json

app = Flask(__name__)

cnn_worldnews = feedparser.parse('http://rss.cnn.com/rss/cnn_world.rss')


@app.route("/")
def main():
    return render_template('index.html')





def loop_through_news(news):
    file = open('/home/skyler/news_aggregator/newsAggregator/data_lists/country-keyword-list.csv', encoding = 'UTF-16')
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
                    print (news.entries[i].title)
        i += 1



loop_through_news(cnn_worldnews)

if __name__ == "__main__":
    app.run()
