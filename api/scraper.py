import bs4
import requests
from unidecode import unidecode
from jdatetime import datetime
from pytz import timezone

url = "https://www.tgju.org/"
HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
tz = timezone('Asia/Tehran')
titles = ['stock', 'ounce', 'mesghal', 'gold', 'coin', 'dollar', 'euro', 'brent', 'bitcoin']


def clean_up(item):
    item = unidecode(item)
    return item


def get_price():
    result = []  # all prices will save in this list after each function call
    try:
        res = requests.get(url, headers=HEADERS)
    except Exception as e:
        print(f"Error :\n{e}")
    else:
        soup = bs4.BeautifulSoup(res.content, "html5lib")
        table = soup.select(".info-bar.mobile-hide")[0]  # first table at top of the site
        prices = table.select(".info-value")  # get all boxes from table(gold, dollar etc)
        changes = table.select(".info-change")
        for title, price, change in zip(titles, prices, changes):
            price_dic = {}
            price_dic['title'] = title
            price_dic['price'] = clean_up(price.select(".info-price")[0].text)  # current price
            price_dic['change'] = clean_up(change.text)  # change rate
            result.append(price_dic)
    return result


class MakeResponse:
    def __init__(self, price):
        self.price = price
        self.time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    def __str__(self):
        return f'Response(price={self.price}, time={self.time}'


if __name__ == "__main__":
    print(get_price())
