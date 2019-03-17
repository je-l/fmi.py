from typing import Callable, Dict, Any, Awaitable

import aiohttp


def authed_fetch(api_key: str) -> Callable[..., Awaitable[bytes]]:
    """Wrap aiohttp request with authorization header
    """

    async def wrapped(url: str, aiohttp_kwargs: Dict[str, Any]) -> bytes:
        aiohttp_kwargs = aiohttp_kwargs or {}

        if aiohttp_kwargs.get("headers"):
            aiohttp_kwargs["headers"]["fmi-apikey"] = api_key
        else:
            aiohttp_kwargs["headers"] = {"fmi-apikey": api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, **aiohttp_kwargs) as response:
                res: bytes = await response.read()
                return res

    return wrapped
