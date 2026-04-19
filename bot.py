import requests
import time
import random

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def get_product(pid):
    url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={pid}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code != 200:
            return None

        data = r.json()
        products = data.get("data", {}).get("products", [])

        if not products:
            return None

        return products[0]

    except:
        return None


def check():
    # случайные товары (перебор базы WB)
    for _ in range(50):
        pid = random.randint(10000000, 200000000)

        if pid in seen:
            continue

        p = get_product(pid)
        if not p:
            continue

        price = p.get("salePriceU", 0) / 100
        price_old = p.get("priceU", 0) / 100

        if price <= 0 or price_old <= 0:
            continue

        discount = 1 - (price / price_old)

        if discount >= 0.7:
            link = f"https://www.wildberries.ru/catalog/{pid}/detail.aspx"

            msg = f"""🔥 АКЦИЯ

Старая цена: {price_old}₽
Цена сейчас: {price}₽
Скидка: {round(discount*100)}%

{link}
"""
            send(msg)
            seen.add(pid)
            print("Найдена акция:", pid)


while True:
    try:
        check()
    except Exception as e:
        print("Ошибка:", e)

    time.sleep(60)
