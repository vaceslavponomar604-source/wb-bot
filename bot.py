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


# --- источник с CDN (не блокируется как search) ---
def fetch_shard(shard=1, page=1):
    # популярный shard, можно перебирать несколько
    url = f"https://basket-01.wb.ru/vol0/data/main/ru/catalog/shard{shard}/{page}.json"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("Ошибка запроса:", e)
        return []

    if r.status_code != 200:
        print("Статус не 200:", r.status_code)
        return []

    try:
        data = r.json()
    except:
        print("Не JSON")
        return []

    return data.get("products", [])


def check_wb():
    products = []

    # берём несколько страниц/шардов
    for shard in [1, 2, 3]:
        for page in [1, 2]:
            products += fetch_shard(shard, page)

    print("Всего товаров:", len(products))

    for p in products:
        product_id = p.get("id")
        price = p.get("salePriceU", 0) / 100

        # тут нет бонусов напрямую → имитируем через скидку
        price_basic = p.get("priceU", 0) / 100

        if not product_id or price <= 0 or price_basic <= 0:
            continue

        if product_id in seen:
            continue

        discount = 1 - (price / price_basic)

        # фильтр ~70% "выгоды"
        if discount >= 0.7:
            link = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"

            msg = f"""🔥 АКЦИЯ (по скидке)

💰 Было: {price_basic}₽
💸 Сейчас: {price}₽
📉 Скидка: {round(discount*100)}%

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
