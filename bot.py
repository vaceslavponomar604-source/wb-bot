import requests
import time

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Ошибка отправки:", e)


def check_wb():
    url = "https://search.wb.ru/exactmatch/ru/common/v5/search"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }

    params = {
        "query": "",
        "resultset": "catalog",
        "sort": "popular",
        "limit": 100
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
    except Exception as e:
        print("Ошибка запроса:", e)
        return

    print("Status:", r.status_code)

    if r.status_code != 200:
        print("WB блокирует или ошибка:", r.text[:200])
        return

    try:
        data = r.json()
    except Exception as e:
        print("Не JSON:", r.text[:200])
        return

    products = data.get("data", {}).get("products", [])

    print("Найдено товаров:", len(products))

    for p in products:
        product_id = p.get("id")
        price = p.get("salePriceU", 0) / 100
        bonus = p.get("saleConditions", {}).get("bonus", 0)

        if not product_id:
            continue

        if product_id in seen:
            continue

        if price > 0 and bonus >= price * 0.7:
            link = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"

            msg = f"""🔥 АКЦИЯ

💰 Цена: {price}₽
🎯 Баллы: {bonus}
📊 {round(bonus/price*100)}%

👉 {link}
"""
            send(msg)
            seen.add(product_id)


while True:
    try:
        check_wb()
    except Exception as e:
        print("Общая ошибка:", e)

    time.sleep(60)
