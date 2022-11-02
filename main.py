import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError
from core.login import login
from bs4 import BeautifulSoup

load_dotenv()


async def run(playwright):
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    page.set_default_timeout(5000)

    netid = os.getenv("netid")
    password = os.getenv("netid_password")

    await page.goto("https://classie-evals.stonybrook.edu/")

    # Trigger Duo SSO
    await login(page, netid, password)
    await asyncio.sleep(5)

    # Select the latest term
    term_box = page.locator("#SearchTerm")
    await term_box.select_option(index=1)

    # Click The Go Button
    await page.click("text=Go")

    while True:
        try:
            await page.wait_for_load_state('domcontentloaded')
            # Extract all classes on current page
            links = page.locator("td a")
            classes = await links.all_inner_texts()
            classes = list(filter(lambda x: x[-1].isnumeric(), classes))
            print(classes)

            await page.screenshot(path="screenshot.png")
            await page.click("text=Next >")
            break
        except TimeoutError:
            url = page.url
            print(url)
            await browser.close()
            break


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())