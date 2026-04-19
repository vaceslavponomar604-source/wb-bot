import time
from playwright.sync_api import sync_playwright
import requests

TOKEN = "ТВОЙ_ТОКЕН"
CHAT_ID = "ТВОЙ_CHAT_ID"

seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def parse_page(page):
    items = page.query_selector_all('[data-widget="searchResultsV2"] a')

    print("Найдено:", len(items))

    for item in items[:30]:
        try:
            link = item.get_attribute("href")
            text = item.inner_text()

            if not link or not text:
                continue

            if link in seen:
                continue

            # примитивный фильтр (потом улучшим)
            if "%" in text:
                msg = f"""🔥 OZON

{text[:200]}

https://www.ozon.ru{link}
"""
                send(msg)
                seen.add(link)

        except:
            continue


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while True:
            try:
                page.goto("https://www.ozon.ru/search/?text=шампунь", timeout=60000)
                time.sleep(5)

                parse_page(page)

            except Exception as e:
                print("Ошибка:", e)

            time.sleep(60)


run()
