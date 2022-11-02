async def login(page, login, password):
    ## Filling in NetID
    await page.fill("text=Username", login)
    await page.fill("text=Password >> nth=1", password)
    await page.locator(".login-button").click()

    ## On push page
    await page.reload()

    # Clicking the send push notification to log in
    frame = await page.query_selector("#duo_iframe")
    content = await frame.content_frame()
    await content.click("button >> nth=0")

    # Wait for me to authenticate
    print("Waiting 5 seconds for DUO Authentication on device ...")