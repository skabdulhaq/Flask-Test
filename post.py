import random
import requests

# #E7E0C9 #C1CFC0 #6B7AA1 #11324D


def post_render() -> list:
    topic = ["investing"]
    news_endpoint = "https://newsapi.org/v2/everything"
    api_key_news = "c5131eefa9ff4e29a00ec04e7947e053"
    param_news = {
        "qInTitle": random.choice(topic),
        "apiKey": api_key_news,
        "pageSize": 50
    }
    response_news = requests.get(news_endpoint, params=param_news)
    all_news = response_news.json()
    all_news_art = all_news["articles"]
    return all_news_art
