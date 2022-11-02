import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from core.login import login

load_dotenv()


async def run(playwright):
    browser = await playwright.chromium.launch()
    page = await browser.new_page()

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

    await page.wait_for_load_state('domcontentloaded')
    await page.screenshot(path="screenshot.png")
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())