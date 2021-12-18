import datetime
import math
import random
import gunicorn
import requests
import live_data
# from live_data import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, redirect
from post import post_render
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from pricealert import price_data


post_p_page = 5

blog_url = "https://api.npoint.io/1f04dd8c4be2ca91e869"
app = Flask(__name__)
app.secret_key = "key"
# all_blogs = requests.get(blog_url).json()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hackathon'
db = SQLAlchemy(app)
admin_uname = "admin@example.com"
admin_pass = "admin"


class Useralerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(12), nullable=False)


def check_everyone():
    search = Useralerts.query.filter_by().all()
    for _ in search:
        price_data(URL_=_.url, name=_.name, email=_.email, set_price=_.price)


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_everyone, trigger="interval", seconds=60*60*24)
scheduler.start()


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    short_description = db.Column(db.String(30), nullable=False)
    full_description = db.Column(db.String(12000), nullable=False)
    author = db.Column(db.String(12), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    image_link = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10))


def save(name, email, url, price):
    entry = Useralerts(name=name,
                       email=email,
                       time=datetime.datetime.now(), url=url,
                       price=price)
    db.session.add(entry)
    db.session.commit()

api_key_stocks = "AU35YGX6GFB5PHT8"
end_point_stock_market = "https://www.alphavantage.co/query"
ALL_INVESTMENTS = ["BTC", "ETH", "BNB", "USDT", "DOGE"]


def live():
    RESULT = [requests.get(url=end_point_stock_market,
                           params={"function": "CURRENCY_EXCHANGE_RATE", "from_currency": investment, "to_currency": "INR",
                                   "apikey": api_key_stocks}).json()["Realtime Currency Exchange Rate"] for investment in ALL_INVESTMENTS]
    return RESULT

# prev = live()

@app.route('/')
def home():
#     global prev
#     if random.randint(1,100) == 6:
#         try:
#             RESULT = live()
#             prev = RESULT
#         except:
#             RESULT = prev
#     else:
#         RESULT = prev
    RESULT = [{'1. From_Currency Code': 'BTC', '2. From_Currency Name': 'Bitcoin', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '3574290.92000000', '6. Last Refreshed': '2021-12-18 12:17:20', '7. Time Zone': 'UTC', '8. Bid Price': '3574290.92000000', '9. Ask Price': '3574291.67976000'}, {'1. From_Currency Code': 'ETH', '2. From_Currency Name': 'Ethereum', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '301652.07136000', '6. Last Refreshed': '2021-12-18 12:18:04', '7. Time Zone': 'UTC', '8. Bid Price': '301659.66896000', '9. Ask Price': '301660.42872000'}, {'1. From_Currency Code': 'BNB', '2. From_Currency Name': 'Binance-Coin', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '40470.54819300', '6. Last Refreshed': '2021-12-18 12:19:09', '7. Time Zone': 'UTC', '8. Bid Price': '40470.54819300', '9. Ask Price': '40470.54819300'}, {'1. From_Currency Code': 'USDT', '2. From_Currency Name': 'Tether', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '76.09155989', '6. Last Refreshed': '2021-12-18 12:19:10', '7. Time Zone': 'UTC', '8. Bid Price': '76.09155989', '9. Ask Price': '76.09155989'}, {'1. From_Currency Code': 'DOGE', '2. From_Currency Name': 'DogeCoin', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '13.12865280', '6. Last Refreshed': '2021-12-18 12:20:14', '7. Time Zone': 'UTC', '8. Bid Price': '13.12105520', '9. Ask Price': '13.12865280'}]
    return render_template("index.html", all_list=RESULT, float=float, round=round)


@app.route("/learning")
def learning():
    return render_template("learning.html")


@app.route("/alert", methods=["POST", "GET"])
def alert():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        url = request.form["url"]
        min_price = request.form["price"]
        save(name, email, url, min_price)
    return render_template("alert.html", message=False)


all_bbs = []


@app.route("/blogs/")
def blog_page():
    global all_bbs
    all_posts = post_render()
    page = request.args.get('page')
    last = math.ceil(len(all_posts) / post_p_page)
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    all_post = all_posts[(page - 1) * post_p_page:(page - 1) * post_p_page + post_p_page]
    all_bbs = all_post
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)
    return render_template("blog.html", blogs=all_post, next=next, prev=prev)


@app.route("/blog/<title>")
def post_page(title):
    global all_bbs
    for blog in all_bbs:
        if blog["title"] == title:
            return render_template("post.html",
                                   image=blog["urlToImage"],
                                   title=title,
                                   sd=blog["description"],
                                   author=blog["author"],
                                   time=blog["publishedAt"],
                                   fd=blog["content"],
                                   url=blog["url"])
    return render_template("post.html")

if __name__ == "__main__":
    app.run()
atexit.register(lambda: scheduler.shutdown())
