import aiohttp


async def get_json_request(url: str, params: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            try:
                json_response = await response.json()
                if response.status == 200:
                    return json_response
            except:
                return {}


async def get_read_request(url: str, params: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            try:
                if response.status == 200:
                    result = await response.read()
                    return result
                else:
                    return None
            except:
                return None


async def post_request(url: str, params: dict, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, data=data):
            pass
