from fmi import Client
import pytest


def test_can_create_new_client():
    Client("aaa")


def test_cannot_use_empty_api_key():
    with pytest.raises(ValueError):
        Client("")


@pytest.mark.asyncio
async def test_cannot_use_five_as_interval():
    c = Client("abc")
    with pytest.raises(ValueError):
        await c.latest_observations("kuopio", timestep=5)


@pytest.mark.asyncio
async def test_sea_levels_invalid_timestep():
    with pytest.raises(ValueError):
        c = Client("123")
        await c.sea_levels(123456, timestep=15)
