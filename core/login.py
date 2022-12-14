async def login(page, login, password, wait):
    ## Filling in NetID
    await page.fill("text=Username", login)
    await page.fill("text=Password >> nth=1", password)
    await page.locator(".login-button").click()

    ## On push page
    await page.reload()

    # Clicking the send push notification to log in
    frame = await page.query_selector("#duo_iframe")
    content = await frame.content_frame()

    # uncomment this; if duo auto send push is not enabled
    # await content.check("input[name=dampen_choice]")
    # await content.click("button >> nth=0")

    # Wait for me to authenticate
    print(f"Waiting {wait} seconds for DUO Authentication on device ...")