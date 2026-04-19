import requests
import time
import random

TOKEN = "ТВОЙ_ТГ_ТОКЕН"
CHAT_ID = "ТВОЙ_CHAT_ID"

seen = set()

HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Linux; Android 10)"
    ]),
    "Accept": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Connection": "keep-alive"
}


def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def fetch():
    url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2"

    params = {
        "url": "/search/?text=шампунь"
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return {}

        return r.json()

    except Exception as e:
        print("Ошибка:", e)
        return {}


def parse(data):
    products = []

    try:
        widgets = data.get("widgetStates", {})

        for key, value in widgets.items():
            if "items" in str(value):
                for item in value.get("items", []):
                    products.append(item)

    except:
        pass

    return products


def check():
    data = fetch()
    items = parse(data)

    print("Найдено:", len(items))

    for item in items:
        try:
            pid = item.get("id")

            price_data = item.get("price", {})
            price = price_data.get("price", 0)
            old_price = price_data.get("oldPrice", 0)

            if not pid or price == 0 or old_price == 0:
                continue

            if pid in seen:
                continue

            discount = 1 - (price / old_price)

            if discount >= 0.7:
                link = f"https://www.ozon.ru/product/{pid}"

                msg = f"""🔥 OZON АКЦИЯ

Цена: {price}₽
Было: {old_price}₽
Скидка: {round(discount*100)}%

{link}
"""
                send(msg)
                seen.add(pid)

        except:
            continue


while True:
    try:
        check()
    except Exception as e:
        print("Ошибка цикла:", e)

    time.sleep(60)
