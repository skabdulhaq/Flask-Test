import math
import requests
from flask import Flask, render_template, request
from post import post_render
import pyrebase
from emailsender import EmailSender
from secrates import email_google
from secrates import password_google


firebaseConfig = {
    "apiKey": "AIzaSyBqg842FDWDh5ZE7ImJ3oBptePQnUgpy4g",
    "authDomain": "let-s-finance.firebaseapp.com",
    "projectId": "let-s-finance",
    "storageBucket": "let-s-finance.appspot.com",
    "messagingSenderId": "106707857115",
    "appId": "1:106707857115:web:32e95cda814008d312a6fe",
    "measurementId": "G-W7MRTG1J4G",
    "databaseURL": "https://let-s-finance-default-rtdb.firebaseio.com/"
}
post_p_page = 5
app = Flask(__name__)
app.secret_key = "key"
api_key_stocks = "AU35YGX6GFB5PHT8"
end_point_stock_market = "https://www.alphavantage.co/query"
ALL_INVESTMENTS = ["BTC", "ETH", "BNB", "USDT", "DOGE"]


def live():
    RESULT = [requests.get(url=end_point_stock_market,
                           params={"function": "CURRENCY_EXCHANGE_RATE", "from_currency": investment, "to_currency": "INR",
                                   "apikey": api_key_stocks}).json()["Realtime Currency Exchange Rate"] for investment in ALL_INVESTMENTS]
    return RESULT


def save(item):
    firebase = pyrebase.initialize_app(firebaseConfig)
    data_base = firebase.database()
    data_base.push(item)

client = EmailSender(email_google, password_google, email_provider="gmail")


def mail_me(name, phone, email, message):
    client.email_send(email_google, f"{name} want to tell something", f"{message}\n {name}'s phone number {phone} and mail : {email}")


@app.route('/')
def home():
    RESULT = [{'1. From_Currency Code': 'BTC', '2. From_Currency Name': 'Bitcoin', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '3574290.92000000', '6. Last Refreshed': '2021-12-18 12:17:20', '7. Time Zone': 'UTC', '8. Bid Price': '3574290.92000000', '9. Ask Price': '3574291.67976000'}, {'1. From_Currency Code': 'ETH', '2. From_Currency Name': 'Ethereum', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '301652.07136000', '6. Last Refreshed': '2021-12-18 12:18:04', '7. Time Zone': 'UTC', '8. Bid Price': '301659.66896000', '9. Ask Price': '301660.42872000'}, {'1. From_Currency Code': 'BNB', '2. From_Currency Name': 'Binance-Coin', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '40470.54819300', '6. Last Refreshed': '2021-12-18 12:19:09', '7. Time Zone': 'UTC', '8. Bid Price': '40470.54819300', '9. Ask Price': '40470.54819300'}, {'1. From_Currency Code': 'USDT', '2. From_Currency Name': 'Tether', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '76.09155989', '6. Last Refreshed': '2021-12-18 12:19:10', '7. Time Zone': 'UTC', '8. Bid Price': '76.09155989', '9. Ask Price': '76.09155989'}, {'1. From_Currency Code': 'DOGE', '2. From_Currency Name': 'DogeCoin', '3. To_Currency Code': 'INR', '4. To_Currency Name': 'Indian Rupee', '5. Exchange Rate': '13.12865280', '6. Last Refreshed': '2021-12-18 12:20:14', '7. Time Zone': 'UTC', '8. Bid Price': '13.12105520', '9. Ask Price': '13.12865280'}]
    return render_template("index.html", all_list=RESULT, float=float, round=round)


@app.route("/quickstart")
def quick_start():
    return render_template("quickstart.html")


@app.route("/resources")
def learning():
    return render_template("learning.html")


@app.route("/guidance")
def guide():
    return render_template("guide.html")


@app.route("/why-to-invest")
def ytolearnpage():
    return render_template("whytoinvest.html")


@app.route("/alert", methods=["POST", "GET"])
def alert():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        url = request.form["url"]
        min_price = request.form["price"]
        packet = {"name": name,
                  "email": email,
                  "url": url,
                  "min": min_price,
                  }
        save(packet)
    return render_template("alert.html", message=False)


all_bbs = []


@app.route("/support", methods=["POST", "GET"])
def support():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        message = request.form["message"]
        mail_me(name, phone, email, message)
        return render_template("support.html", message=True)
    return render_template("support.html")


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
        next_ = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next_ = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next_ = "/?page=" + str(page + 1)
    return render_template("blog.html", blogs=all_post, next=next_, prev=prev)


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
    app.run(debug=True)
