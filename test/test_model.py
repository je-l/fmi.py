from fmi.model import Observation


def test_return_none_if_zero_wawa():
    o = Observation(wawa=0)
    assert o.verbal() is None


def test_return_sumua_if_weather_code_30():
    o = Observation(wawa=30)
    assert o.verbal() == "sumua"
