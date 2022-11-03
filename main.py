import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError
from core.login import login
from core.page import extract_data
from json import dumps, loads

load_dotenv()


async def run(playwright):
    # Playwright Setup
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    page.set_default_timeout(10000)

    netid = os.getenv("netid")
    password = os.getenv("netid_password")
    base_url = "https://classie-evals.stonybrook.edu"

    await page.goto(base_url)

    # Trigger Duo SSO
    sleep = 5
    await login(page, netid, password, sleep)
    await asyncio.sleep(sleep)

    # Simple cache
    cache_file = ".cache"
    loaded_cache = False
    try:
        with open(cache_file, "r") as f:
            curr = f.readline()
            if not curr:
                # Select the term
                # index 1 will be the most recent term
                term_box = page.locator("#SearchTerm")
                await term_box.select_option(index=2)

                # Click The Go Button
                await page.click("text=Go")
            else:
                await page.goto(curr)
                loaded_cache = True
    except FileNotFoundError:
        term_box = page.locator("#SearchTerm")
        await term_box.select_option(index=2)

        # Click The Go Button
        await page.click("text=Go")
    term = await page.locator("h2").inner_text()

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
                # Fastforward to the latest entry on the page
                if loaded_cache:
                    with open("data.json", "r") as f:
                        sec = loads(f.readlines()[-1])["Section"]
                        if cls == sec:
                            loaded_cache = False
                        continue
                # Go to the class specific page
                element = page.locator(f"text={cls}")
                count = await element.count()

                with open("data.json", "a+") as f:
                    if count > 1 and cls not in visited:
                        for i in range(count):
                            url = await element.nth(i).get_attribute("href")
                            await page.goto(f"{base_url}{url}")

                            write_data = await extract_data(page, cls, term)
                            f.write(dumps(write_data) + "\n")
                            await page.goto(current_page)

                        visited.add(cls)
                    elif count > 1:
                        continue
                    else:
                        url = await element.get_attribute("href")
                        await page.goto(f"{base_url}{url}")

                        write_data = await extract_data(page, cls, term)
                        f.write(dumps(write_data) + "\n")
                await page.goto(current_page)

            # Navigate to next page
            await page.click("text=Next >")
        except TimeoutError as e:
            print(f"{e}\nVerify that last page is: {page.url}")
            # Saves the current page into cache
            with open(cache_file, "w+") as f:
                f.write(current_page)
            await browser.close()
            break


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())