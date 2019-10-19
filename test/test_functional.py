import fmi
import pytest


@pytest.mark.asyncio
@pytest.mark.slow
async def test_temp_for_helsinki():
    w = await fmi.weather_now("helsinki")

    assert -50 < w.temperature < 50


@pytest.mark.asyncio
@pytest.mark.slow
async def test_invalid_place():
    with pytest.raises(ValueError):
        await fmi.weather_now("asdfasdfasdf")
