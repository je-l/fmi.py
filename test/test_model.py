from fmi.model import Observation


def test_return_none_if_zero_wawa():
    obs = Observation(wawa=0)
    assert obs.weather_text is None


def test_return_sumua_if_weather_code_30():
    obs = Observation(wawa=30)
    assert obs.weather_text == "sumua"
