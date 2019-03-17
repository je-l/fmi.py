from fmi.model import Observation, Coordinates


def test_return_none_if_zero_wawa():
    obs = Observation(Coordinates(60.2, 24.2), 50.0, 20.2, 1.1, 123, wawa=0)
    assert obs.weather_text is None


def test_return_sumua_if_weather_code_30():
    obs = Observation(Coordinates(60.2, 24.2), 50.0, 20.2, 1.1, 123, wawa=30)
    assert obs.weather_text == "sumua"
