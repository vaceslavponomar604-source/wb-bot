import requests
import time

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def check_wb():
    url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
    params = {
        "query": "",
        "resultset": "catalog",
        "sort": "popular",
        "limit": 50
    }

    r = requests.get(url, params=params).json()
    products = r.get("data", {}).get("products", [])

    for p in products:
        product_id = p.get("id")
        price = p.get("salePriceU", 0) / 100
        bonus = p.get("saleConditions", {}).get("bonus", 0)

        if product_id in seen:
            continue

        if price > 0 and bonus >= price * 0.7:
            link = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"

            msg = f"🔥 Акция\nЦена: {price}₽\nБаллы: {bonus}\n👉 {link}"
            send(msg)
            seen.add(product_id)

while True:
    try:
        check_wb()
    except Exception as e:
        print(e)

    time.sleep(60)
