import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError
from core.login import login
from core.page import extract_data
from pymongo import MongoClient

load_dotenv()


async def run(playwright):
    # Playwright Setup
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    page.set_default_timeout(5000)

    netid = os.getenv("netid")
    password = os.getenv("netid_password")
    base_url = "https://classie-evals.stonybrook.edu/"

    await page.goto(base_url)

    # Trigger Duo SSO
    sleep = 5
    await login(page, netid, password, sleep)
    await asyncio.sleep(sleep)

    # Select the latest term
    term_box = page.locator("#SearchTerm")
    await term_box.select_option(index=2)

    # Click The Go Button
    await page.click("text=Go")
    term = await page.locator("h2").inner_text()

    # Mongo Setup
    client = MongoClient(os.getenv("mongo_url"))
    db = client.get_database("Gradus")
    collection = db.get_collection(term)

    while True:
        try:
            await page.wait_for_load_state('domcontentloaded')
            current_page = page.url
            # Extract all classes on current page
            links = page.locator("td a")
            classes = await links.all_inner_texts()
            classes = list(filter(lambda x: x[-1].isnumeric(), classes))
            visited = set()

            for cls in classes:
                # Go to the class specific page
                element = page.locator(f"text={cls}")
                count = await element.count()

                if count > 1 and cls not in visited:
                    for i in range(count):
                        url = await element.nth(i).get_attribute("href")
                        await page.goto(f"{base_url}{url}")

                        write_data = await extract_data(page, cls, term)
                        collection.insert_one(write_data)
                        print(write_data)
                        await page.goto(current_page)

                    visited.add(cls)
                elif count > 1:
                    continue
                else:
                    url = await element.get_attribute("href")
                    await page.goto(f"{base_url}{url}")

                    write_data = await extract_data(page, cls, term)
                    collection.insert_one(write_data)
                    print(write_data)

                await page.goto(current_page)

            # Navigate to next page
            await page.click("text=Next >")
        except TimeoutError as e:
            print(f"{e}\nVerify that last page is: {page.url}")
            await browser.close()
            break


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())