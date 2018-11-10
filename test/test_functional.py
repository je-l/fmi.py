import fmi
import pytest
from os import environ

is_pull_request = (
    environ.get("TRAVIS") == "true"
    and not environ.get("TRAVIS_PULL_REQUEST") == "false"
)

if is_pull_request:
    pytest.skip(
        "can't run slow tests in pull requests (no api key)",
        allow_module_level=True,
    )


@pytest.mark.asyncio
@pytest.mark.slow
async def test_temp_for_helsinki(real_client):
    w = await real_client.weather_now("helsinki")

    assert -50 < w.temperature < 50


@pytest.mark.asyncio
@pytest.mark.slow
async def test_invalid_place(real_client):
    with pytest.raises(ValueError):
        await real_client.weather_now("asdfasdfasdf")
