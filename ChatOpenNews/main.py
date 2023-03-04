import json
import os

from NewsAPI.NewsAPI import NewsAPI
from OpenAI.OpenAPI import OpenAI
from FrontEnd.CreateLayout import HTMLMaker

from app_secrets import OpenAIAPIKey, NewsAPIKey

script_dir = os.path.dirname(os.path.abspath(__file__))


def write_to_html(articles, settings):
    maker = HTMLMaker(settings)
    maker.create_html(articles)


def openai_analyze(articles, settings):
    open_ai = OpenAI(settings, OpenAIAPIKey)
    for article in articles:
        open_ai.process_article(article)
    return articles


def get_raw_news(settings):
    news_api = NewsAPI(settings, NewsAPIKey)
    news_api.filter_sources()

    headlines = news_api.get_headlines()
    all_news = news_api.get_all_articles()

    with open("headlines.json", "w") as outfile:
        outfile.write(json.dumps(headlines))
    with open("all_news.json", "w") as outfile:
        outfile.write(json.dumps(all_news))

    return headlines, all_news


def get_settings():
    with open(script_dir + "Settings.json", 'w') as file:
        settings = json.load(file)
        return settings


def main():
    settings = get_settings()

    headlines, all_news = get_raw_news(settings["NewsAPI"])

    headlines, all_news = openai_analyze(headlines, settings["OpenAI"]), openai_analyze(all_news, settings["OpenAI"])

    write_to_html(headlines + all_news, settings["FrontEnd"])


if __name__ == "__main__":
    main()
