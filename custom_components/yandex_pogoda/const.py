"""General constants."""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.components.weather import (
    ATTR_WEATHER_TEMPERATURE_UNIT,
    ATTR_WEATHER_WIND_SPEED_UNIT,
    UNIT_CONVERSIONS,
)
from homeassistant.const import Platform

DOMAIN = "yandex_pogoda"
DEFAULT_NAME = "Yandex Pogoda"
DEFAULT_UPDATES_PER_DAY = 12
ATTRIBUTION = "Data provided by Yandex Pogoda"
MANUFACTURER = "Yandex"
ENTRY_NAME = "name"
UPDATER = "updater"

API_DAY_PARTS = (("night", 2), ("morning", 9), ("day", 15), ("evening", 20))

ATTR_API_TEMPERATURE = "temperature"
ATTR_API_FEELS_LIKE_TEMPERATURE = "feelsLike"
ATTR_API_WIND_SPEED = "windSpeed"
ATTR_API_WIND_BEARING = "windAngle"
ATTR_WIND_BEARING_DIRECTION = "wind_direction"

ATTR_API_DAYTIME = "daytime"
ATTR_API_CONDITION = "condition"
ATTR_API_IMAGE = "icon"
ATTR_API_SERVER_TIME = "serverTime"
ATTR_API_TIME = "time"
ATTR_API_YA_CONDITION = "yandex_condition"
ATTR_API_WIND_GUST = "windGust"
ATTR_MIN_FORECAST_TEMPERATURE = "min_forecast_temperature"
ATTR_API_FORECAST_ICONS = "forecast_icons"

ATTR_FORECAST_DATA = "forecast"

CONF_LANGUAGE_KEY = "language"
UPDATE_LISTENER = "update_listener"
PLATFORMS = [Platform.SENSOR, Platform.WEATHER]

WEATHER_STATES_CONVERSION = {
    "CLEAR": {
        "day": "sunny",
        "night": "clear-night",
    },
    "PARTLY_CLOUDY": "partlycloudy",
    "CLOUDY": "cloudy",
    "OVERCAST": "cloudy",
    "LIGHT_RAIN": "rainy",
    "RAIN": "rainy",
    "HEAVY_RAIN": "pouring",
    "SHOWERS": "pouring",
    "SLEET": "snowy-rainy",
    "LIGHT_SNOW": "snowy",
    "SNOW": "snowy",
    "SNOWFALL": "snowy",
    "HAIL": "hail",
    "THUNDERSTORM": "lightning",
    "THUNDERSTORM_WITH_RAIN": "lightning-rainy",
    "THUNDERSTORM_WITH_HAIL": "lightning-rainy",
}
"""Map rich Yandex weather condition to ordinary HA"""

CONDITION_ICONS = {
    "CLEAR": {
        "day": "mdi:weather-sunny",
        "night": "mdi:weather-night",
    },
    "PARTLY_CLOUDY": {
        "day": "mdi:weather-partly-cloudy",
        "night": "mdi:weather-night-partly-cloudy",
    },
    "CLOUDY": "mdi:weather-cloudy",
    "OVERCAST": "mdi:weather-cloudy",
    "LIGHT_RAIN": "mdi:weather-rainy",
    "RAIN": "mdi:weather-rainy",
    "HEAVY_RAIN": "mdi:weather-pouring",
    "SHOWERS": "mdi:weather-pouring",
    "SLEET": "mdi:weather-snowy-rainy",
    "LIGHT_SNOW": "mdi:weather-snowy",
    "SNOW": "mdi:weather-snowy",
    "SNOWFALL": "mdi:weather-snowy-heavy",
    "HAIL": "mdi:weather-hail",
    "THUNDERSTORM": "mdi:weather-lightning",
    "THUNDERSTORM_WITH_RAIN": "mdi:weather-lightning-rainy",
    "THUNDERSTORM_WITH_HAIL": "mdi:weather-lightning-rainy",
}
"""Mapping for state icon"""

TEMPERATURE_CONVERTER = UNIT_CONVERSIONS[ATTR_WEATHER_TEMPERATURE_UNIT]
WIND_SPEED_CONVERTER = UNIT_CONVERSIONS[ATTR_WEATHER_WIND_SPEED_UNIT]
WIND_DIRECTION_MAP = {
    0.0: "N",
    22.5: "NNE",
    45.0: "NE",
    67.5: "ENE",
    90.0: "E",
    112.5: "ESE",
    135.0: "SE",
    157.5: "SSE",
    180.0: "S",
    202.5: "SSW",
    225.0: "SW",
    247.5: "WSW",
    270.0: "W",
    292.5: "WNW",
    315.0: "NW",
    337.5: "NNW",
    360.0: "N",
}


def convert_unit_value(
    converter: Callable[[float, str, str], float],
    val: float,
    unit_from: str,
    unit_to: str,
) -> float | None:
    """Weather factor unit converter."""
    if val is not None and unit_from and unit_to:
        return converter(val, unit_from, unit_to)
    return None


def map_state(src: str, is_day: bool, mapping: dict | None = None) -> str:
    """Map weather condition based on WEATHER_STATES_CONVERSION.

    :param src: str: Yandex weather state
    :param is_day: bool: Is it day? Used for icons
    :param mapping: use this dict for mapping
    :return: str: Home Assistant weather state
    """
    if mapping is None:
        mapping = {}

    try:
        result: str | dict[str, str] = mapping[src]
    except KeyError:
        result = src

    if type(result) is dict:
        return result["day" if is_day else "night"]

    return result


def round_by_part(value: int | float, part: int | float) -> int | float:
    """Round value to parts

    :param value: value to round
    :param part: part with which value is rounded
    :return: rounded value
    """
    if part <= 0:
        raise ValueError("Part must be greater than zero")

    return round(value / float(part)) * part


def get_wind_direction(wind_angle: int) -> int | float:
    """Get wind direction from windAngle"""

    if wind_angle < 0 or wind_angle > 360:
        raise ValueError("Angle should be in [0; 360] range")

    return WIND_DIRECTION_MAP[round_by_part(wind_angle, 22.5)]
