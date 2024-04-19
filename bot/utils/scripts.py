import aiohttp


async def get_request(url: str, params: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            try:
                json_response = await response.json()
                if response.status == 200:
                    return json_response
            except:
                return {}


async def post_request(url: str, params: dict, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, data=data):
            pass
