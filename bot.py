import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

URL = "https://www.ozon.ru/search/?text=шампунь"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page = await context.new_page()

        # ВАЖНО — вот правильный stealth
        await stealth_async(page)

        print("Открываю страницу...")
        await page.goto(URL, timeout=60000)

        await page.wait_for_timeout(5000)

        links = await page.query_selector_all("a[href*='/product/']")

        print(f"Найдено ссылок: {len(links)}")

        await browser.close()

asyncio.run(main())
