import fmi
import pytest


@pytest.mark.asyncio
async def test_cannot_use_five_as_interval():
    with pytest.raises(ValueError):
        await fmi.latest_observations("kuopio", timestep=5)


@pytest.mark.asyncio
async def test_sea_levels_invalid_timestep():
    with pytest.raises(ValueError):
        await fmi.sea_levels(123456, timestep=15)
