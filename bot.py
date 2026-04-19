import requests
import time

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

# 👇 ВСТАВЬ СЮДА АРТИКУЛЫ WB (что реально важно тебе)
PRODUCTS = [
    12345678,
    87654321,
    11223344
]

seen = {}

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def get_product(pid):
    url = f"https://card.wb.ru/cards/detail?nm={pid}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code != 200:
            print("Ошибка WB:", r.status_code)
            return None

        data = r.json()
        products = data.get("data", {}).get("products", [])
        if not products:
            return None

        return products[0]

    except Exception as e:
        print("Ошибка:", e)
        return None


def check():
    for pid in PRODUCTS:
        p = get_product(pid)
        if not p:
            continue

        price = p.get("salePriceU", 0) / 100
        old_price = p.get("priceU", 0) / 100

        if price <= 0 or old_price <= 0:
            continue

        discount = 1 - (price / old_price)

        # проверяем изменение
        prev_price = seen.get(pid)

        if prev_price != price:
            seen[pid] = price

            # фильтр 70%
            if discount >= 0.7:
                link = f"https://www.wildberries.ru/catalog/{pid}/detail.aspx"

                msg = f"""🔥 АКЦИЯ ОБНАРУЖЕНА

Товар: {pid}
Старая цена: {old_price}₽
Цена сейчас: {price}₽
Скидка: {round(discount*100)}%

{link}
"""
                send(msg)
                print("Отправлено:", pid)


while True:
    try:
        check()
    except Exception as e:
        print("Ошибка цикла:", e)

    time.sleep(60)
