import aiohttp


async def fetch(url, **aiohttp_kwargs):
    """Perform HTTP get request
    :param url: fetch target url
    :param aiohttp_kwargs: keyword arguments for aiohttp session.get method
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **aiohttp_kwargs) as response:
            return await response.read()
