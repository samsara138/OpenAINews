import os

import requests
from newsapi import NewsApiClient
import json
from bs4 import BeautifulSoup
import string


def keep_human_readable_ascii(text):
    """
    Keep only human-readable ASCII characters from the given text.
    """
    printable = set(string.printable)
    return ''.join(char for char in text if char in printable)


class NewsAPI:
    sources = []
    api_key = ""
    settings = None
    newsapi = None

    def __init__(self, settings, NewsAPIKey):
        self.sources = []
        self.settings = settings
        self.api_key = NewsAPIKey
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def filter_sources(self):
        source_settings = self.settings["Sources"]
        sources = self.newsapi.get_sources()
        for source in sources["sources"]:
            if all([not source_settings["Categories"] or source["category"] in source_settings["Categories"],
                    not source_settings["Languages"] or source["language"] in source_settings["Languages"],
                    not source_settings["Countries"] or source["country"] in source_settings["Countries"]]):
                self.sources.append(source)

    def get_headlines(self, count=10):
        count = self.settings["NewsCount"]["HeadlineCounts"]
        source_ids = ",".join([source["id"] for source in self.sources])
        keywords = self.settings["Keywords"]
        articles = []
        for keyword in keywords:
            articles += self.newsapi.get_top_headlines(q=keyword, sources=source_ids)["articles"]
        clean_articles = self.clean_articles(articles[:count])
        self.add_raw_to_articles(clean_articles)
        return clean_articles

    def get_all_articles(self):
        count = self.settings["NewsCount"]["GeneralCounts"]
        source_ids = ",".join([source["id"] for source in self.sources])
        keywords = self.settings["Keywords"]
        articles = []
        for keyword in keywords:
            articles += self.newsapi.get_everything(q=keyword, sources=source_ids)["articles"]
        clean_articles = self.clean_articles(articles[:count])
        self.add_raw_to_articles(clean_articles)
        return clean_articles

    def add_raw_to_articles(self, articles):
        for article in articles:
            url = article.get("url", "")
            if url:
                raw = self.get_raw_data(url)
                raw_content = " ".join(raw)
                raw_content = "" if len(" ".join(raw)) < 1000 else raw_content
                article["raw_content"] = raw_content

    @staticmethod
    def get_raw_data(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.find_all('p')
        return [p.text for p in content]

    @staticmethod
    def clean_articles(raw_articles):
        clean_articles = []
        for article in raw_articles:
            clean_article = {
                "source": article["source"]["name"],
                "author": article["author"],
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "image": article["urlToImage"],
                "publish_date": article["publishedAt"],
                "content": article["content"],
            }
            clean_articles.append(clean_article)
        return clean_articles
