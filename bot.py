import requests
import time

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

seen = set()

# ⚠️ ВСТАВЬ СЮДА ПРОКСИ
PROXY = "http://username:password@host:port"
# если нет — оставь None
# PROXY = None


def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Ошибка отправки:", e)


def check_wb():
    url = "https://search.wb.ru/exactmatch/ru/common/v5/search"

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Referer": "https://www.wildberries.ru/",
        "Connection": "keep-alive"
    }

    params = {
        "query": "",
        "resultset": "catalog",
        "sort": "popular",
        "limit": 50
    }

    proxies = {"http": PROXY, "https": PROXY} if PROXY else None

    try:
        r = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=10)
    except Exception as e:
        print("Ошибка запроса:", e)
        return

    print("Status:", r.status_code)

    if r.status_code != 200:
        print("WB блокирует:", r.text[:100])
        return

    try:
        data = r.json()
    except:
        print("Не JSON:", r.text[:100])
        return

    products = data.get("data", {}).get("products", [])

    print("Товаров:", len(products))

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
