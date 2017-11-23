import aiohttp


def authed_fetch(api_key):
    """Wrap aiohttp request with authorization header
    :param api_key: fmi api key
    :rtype coroutine:
    """
    async def wrapped(url, **aiohttp_kwargs):
        if aiohttp_kwargs.get("headers"):
            aiohttp_kwargs["headers"]["fmi-apikey"] = api_key
        else:
            aiohttp_kwargs["headers"] = {"fmi-apikey": api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, **aiohttp_kwargs) as response:
                return await response.read()

    return wrapped
