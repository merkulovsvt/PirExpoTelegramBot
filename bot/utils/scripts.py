import aiohttp


async def request_json(url: str, params: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            json_response = await response.json()
            if response.status == 200:
                return json_response
            else:
                return {}
