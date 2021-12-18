import requests


def data_crypto():
    api_key_stocks = "AU35YGX6GFB5PHT8"
    end_point_stock_market = "https://www.alphavantage.co/query"
    ALL_INVESTMENTS = ["BTC", "ETH", "BNB", "USDT", "DOGE"]
    RESULT = []
    for investment in ALL_INVESTMENTS:
        PARA_stocks = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": investment,
            "to_currency": "INR",
            "apikey": api_key_stocks
        }
        response = requests.get(url=end_point_stock_market, params=PARA_stocks)
        # print(response.json())
        # print(response.json()["Realtime Currency Exchange Rate"])
        RESULT.append(response.json()["Realtime Currency Exchange Rate"])
    return RESULT
# print(data_crypto())