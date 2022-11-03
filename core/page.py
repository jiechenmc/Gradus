from json import dumps


async def extract_data(page, cls, term):
    # Obtaining data and parsing it into a dictionary
    td = page.locator("table").first.locator("td")
    data = await td.all_inner_texts()

    keys = data[::2]
    values = map(int, data[1::2])

    title = await page.locator("h2").inner_text()
    professors = await page.locator("h2 + h3").inner_text()

    write_data = {
        "Section": cls,
        "Term": term,
        "Course Title": title,
        "Instructors": professors,
        "Grades": dict(zip(keys, values))
    }

    return write_data


async def nav_and_extract(page, nav, cls, term, f):
    await page.goto(nav)
    write_data = await extract_data(page, cls, term)
    f.write(dumps(write_data) + "\n")