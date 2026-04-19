import asyncio
from playwright.async_api import async_playwright


async def main():
    url = "https://www.ozon.ru/category/bytovaya-himiya-25000/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Открываю страницу...")
        await page.goto(url, timeout=60000)

        await page.wait_for_timeout(5000)

        # собираем товары
        items = await page.query_selector_all("a[href*='/product/']")

        print(f"Найдено ссылок: {len(items)}")

        for i, item in enumerate(items[:10]):
            link = await item.get_attribute("href")
            print(f"{i+1}: https://www.ozon.ru{link}")

        await browser.close()


asyncio.run(main())
