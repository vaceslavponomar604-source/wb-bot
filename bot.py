import requests
import time

TOKEN = "8676074977:AAE9cgZtDvpSJW8NXDlH4EQBYuI-3K8NRfA"
CHAT_ID = "798337490"

seen = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Accept": "application/json",
    "Referer": "https://www.wildberries.ru/"
}

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def fetch():
    url = "https://search.wb.ru/exactmatch/ru/common/v5/search"

    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "query": "",
        "resultset": "catalog",
        "sort": "popular",
        "limit": 100
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return []

        data = r.json()
        return data.get("data", {}).get("products", [])

    except Exception as e:
        print("Ошибка:", e)
        return []


def check():
    products = fetch()

    print("Найдено:", len(products))

    for p in products:
        pid = p.get("id")

        price = p.get("salePriceU", 0) / 100
        bonus = p.get("feedbackPoints", 0)  # 🔥 ключевое поле

        if not pid or price <= 0 or bonus <= 0:
            continue

        if pid in seen:
            continue

        # условие: баллы ≥ 70% цены
        if bonus >= price * 0.7:
            link = f"https://www.wildberries.ru/catalog/{pid}/detail.aspx"

            msg = f"""🔥 БАЛЛЫ ЗА ОТЗЫВ

Цена: {price}₽
Баллы: {bonus}
Процент: {round((bonus/price)*100)}%

{link}
"""
            send(msg)
            seen.add(pid)
            print("Отправлено:", pid)


while True:
    try:
        check()
    except Exception as e:
        print("Ошибка цикла:", e)

    time.sleep(60)
