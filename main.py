import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()


async def run(playwright):
    webkit = playwright.webkit
    browser = await webkit.launch()
    context = await browser.new_context()
    page = await context.new_page()

    login = os.getenv("netid")
    password = os.getenv("netid_password")

    await page.goto("https://classie-evals.stonybrook.edu/")
    await page.screenshot(path="screenshot.png")
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())