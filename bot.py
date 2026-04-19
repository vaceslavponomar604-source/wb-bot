import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


async def main():
    url = "https://www.ozon.ru/category/bytovaya-himiya-25000/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="ru-RU"
        )

        page = await context.new_page()
        await stealth_async(page)

        print("Открываю страницу...")
        await page.goto(url, timeout=60000)

        await page.wait_for_timeout(7000)

        items = await page.query_selector_all("a[href*='/product/']")

        print(f"Найдено ссылок: {len(items)}")

        for i, item in enumerate(items[:10]):
            link = await item.get_attribute("href")
            print(f"{i+1}: https://www.ozon.ru{link}")

        await browser.close()


asyncio.run(main())
