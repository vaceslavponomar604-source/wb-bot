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


def fetch():
    url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    params = {
        "query": "",
        "resultset": "catalog",
        "limit": 50
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        print("STATUS:", r.status_code)
    except Exception as e:
        print("Ошибка запроса:", e)
        return []

    if r.status_code != 200:
        print("WB блокирует:", r.text[:200])
        return []

    try:
        data = r.json()
    except:
        print("Не JSON")
        return []

    return data.get("data", {}).get("products", [])


def check():
    products = fetch()

    for p in products:
        pid = p.get("id")
        price = p.get("salePriceU", 0) / 100
        bonus = p.get("salePrice", 0) / 100

        if not pid or price <= 0:
            continue

        if pid in seen:
            continue

        if bonus >= price * 0.7:
            link = f"https://www.wildberries.ru/catalog/{pid}/detail.aspx"

            msg = f"""🔥 АКЦИЯ

Цена: {price}₽
Баллы: {bonus}
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
