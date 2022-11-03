from json import loads


async def fast_forward(cls):
    with open("data.json", "r") as f:
        sec = loads(f.readlines()[-1])["Section"]
        if cls == sec:
            return False
        return True
