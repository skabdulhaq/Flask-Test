import requests
from bs4 import BeautifulSoup
import smtplib
from secrates import password_google
from secrates import email_google
import pyrebase

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


def email_send(from_email, password, to_email, subject_, message_):
    postman = smtplib.SMTP(host="smtp.gmail.com", port=587)
    postman.starttls()
    postman.login(user=from_email, password=password)
    postman.sendmail(from_addr=from_email, to_addrs=to_email, msg=f"Subject:{subject_}\n\n{message_}")
    postman.close()


def scraper(url):
    global title
    head = {
        "Accept - Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 "
                      "Safari/537.36 Edg/95.0.1020.40"
    }
    response = requests.get(url=url, headers=head)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find(name="span", class_="a-offscreen")
    title = soup.title.text.split(":")[0]
    # try:
    current_price = float(price.text.split("$")[-1])
    # except ValueError :
    #     current_price = float(price.text.split()[-1])
    return current_price


def ok_to_buy(current_price, set_price):
    if current_price < set_price:
        return True
    else:
        return False


def price_data(URL_, name, email, set_price):
    current_price_ = scraper(URL_)
    api_key_stocks = "AU35YGX6GFB5PHT8"
    end_point_stock_market = "https://www.alphavantage.co/query"
    PARA_stocks = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "USD",
        "to_currency": "INR",
        "apikey": api_key_stocks
    }
    response = requests.get(url=end_point_stock_market, params=PARA_stocks)
    # usd_1 = response.json()["5. Exchange Rate"]
    out = response.json()
    usd_1_n = out["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    usd_1 = float(usd_1_n)
    converted_price = set_price/usd_1
    print(f"cp:{current_price_}\nsp-cp:{converted_price}\nsp:{set_price}")
    if ok_to_buy(current_price_, converted_price):
        subject = f"Your Product on Amazon is at lowest price check it out"
        message = f"{name}\n{title}\n is At lowest price \nTarget price Was {set_price}\n" \
                  f"current_price is {current_price_} go and buy now\n{URL_}"
        email_send(email_google, password_google, email, subject, message)
        return True


def delete():
    pass

firebase = pyrebase.initialize_app(firebaseConfig)
data_base = firebase.database()

all_data = data_base.get().val()
persons = []
# [{'email': 'sk.abdulhaq2004@gmail.com', 'min': '1500', 'name': 'Sk.abdul Haq', 'url': 'https://www.amazon.com/SanDisk-Cruzer-Ultra-Flash-SDCZ48-016G-U46/dp/B00NIEIRVY/ref=sr_1_10?crid=1CAP6BWZ3J8ZR&keywords=pendrive+16gb&qid=1636172112&qsid=141-3479514-3048334&refinements=p_89%3ASanDisk%2Cp_n_size_browse-bin%3A1259715011%2Cp_n_feature_keywords_five_browse-bin%3A7688215011%2Cp_n_feature_keywords_two_browse-bin%3A6931972011&rnid=6931969011&s=pc&sprefix=pendriv'}]
for _ in all_data:
    # print(_)
    persons.append(all_data[_])
# t = [False, True]#, True, True, False]
for person in persons:
    if price_data(URL_=person["url"], name=person["name"], email=person["email"], set_price=person["min"]):
        for key in all_data:
            if all_data[key] == person:
                data_base.child(key).remove()
