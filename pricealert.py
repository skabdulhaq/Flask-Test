import requests
from bs4 import BeautifulSoup
import smtplib
from secrates import password_google
from secrates import email_google


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
