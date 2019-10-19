from typing import Callable, Dict, Any, Awaitable

import aiohttp


def authed_fetch() -> Callable[..., Awaitable[bytes]]:
    """Wrap aiohttp request with authorization header
    """

    async def wrapped(url: str, aiohttp_kwargs: Dict[str, Any]) -> bytes:
        aiohttp_kwargs = aiohttp_kwargs or {}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, **aiohttp_kwargs) as response:
                res: bytes = await response.read()
                return res

    return wrapped
