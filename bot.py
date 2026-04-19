import requests
import time

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

seen = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def fetch():
    url = "https://api.ozon.ru/composer-api.bx/page/json/v2"

    params = {
        "url": "/category/elektronika-15500/?sort=score"
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return []

        return r.json()

    except Exception as e:
        print("Ошибка:", e)
        return {}


def parse(data):
    products = []

    try:
        widgets = data.get("widgetStates", {})

        for key in widgets:
            block = widgets[key]

            if "items" in str(block):
                for item in block.get("items", []):
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
            price = item.get("price", {}).get("price", 0)
            old_price = item.get("price", {}).get("oldPrice", 0)
            bonus = item.get("price", {}).get("cardPrice", 0)  # условный бонус

            if not pid or price == 0:
                continue

            if pid in seen:
                continue

            # считаем "выгоду"
            if old_price > 0:
                discount = 1 - (price / old_price)
            else:
                discount = 0

            # фильтр ~70%
            if discount >= 0.7:
                link = f"https://www.ozon.ru/product/{pid}"

                msg = f"""🔥 АКЦИЯ OZON

Цена: {price}₽
Было: {old_price}₽
Скидка: {round(discount*100)}%

{link}
"""
                send(msg)
                seen.add(pid)

        except Exception as e:
            continue


while True:
    try:
        check()
    except Exception as e:
        print("Ошибка цикла:", e)

    time.sleep(60)
