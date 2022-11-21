from json import dumps


async def extract_data(page, cls, term):
    # Check if grade distribution data is available
    first_chart_heading = await page.locator("h4").first.inner_text()

    # Obtaining data and parsing it into a dictionary
    td = page.locator("table").first.locator("td")
    data = await td.all_inner_texts()

    keys = data[::2]
    values = map(int, data[1::2])

    title = await page.locator("h2").inner_text()
    professor = await page.locator("h2 + h3").inner_text()

    if first_chart_heading != "Grade Data Unavailable":
        write_data = {
            "section": cls,
            "term": term,
            "courseTitle": title,
            "instructor": professor,
            "grades": dict(zip(keys, values))
        }
    else:
        write_data = {
            "section": cls,
            "term": term,
            "courseTitle": title,
            "instructor": professor,
            "grades": {}
        }

    return write_data


async def nav_and_extract(page, nav, cls, term, f):
    await page.goto(nav)
    write_data = await extract_data(page, cls, term)
    f.write(dumps(write_data) + "\n")