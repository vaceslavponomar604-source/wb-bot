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


def fetch_products():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    products = []

    # несколько источников (чтобы точно работало)
    urls = [
        "https://basket-01.wb.ru/vol0/data/main/ru/catalog/shard1/1.json",
        "https://basket-02.wb.ru/vol0/data/main/ru/catalog/shard2/1.json",
        "https://basket-03.wb.ru/vol0/data/main/ru/catalog/shard3/1.json"
    ]

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            print("STATUS:", r.status_code)

            if r.status_code != 200:
                continue

            data = r.json()
            products += data.get("products", [])

        except Exception as e:
            print("Ошибка:", e)

    print("Всего товаров:", len(products))
    return products


def check():
    products = fetch_products()

    for p in products:
        pid = p.get("id")
        price = p.get("salePriceU", 0) / 100
        price_old = p.get("priceU", 0) / 100

        if not pid or price <= 0 or price_old <= 0:
            continue

        if pid in seen:
            continue

        discount = 1 - (price / price_old)

        if discount >= 0.7:  # 70% выгоды
            link = f"https://www.wildberries.ru/catalog/{pid}/detail.aspx"

            msg = f"""🔥 НАЙДЕНА АКЦИЯ

Старая цена: {price_old}₽
Цена сейчас: {price}₽
Скидка: {round(discount*100)}%

{link}
"""
            send(msg)
            seen.add(pid)


while True:
    try:
        check()
    except Exception as e:
        print("Общая ошибка:", e)

    time.sleep(60)
