import os
import pytest

from pymaps import Map


API_KEY = os.environ['MAPS_API_KEY']


def test_instanciate_map():
    map = Map(api_key=API_KEY)
    assert isinstance(map, Map)


def test_map_raise_valueerror_without_api_key():
    with pytest.raises(ValueError):
        map = Map()


def test_initial_location_set_to_zero():
    map = Map(api_key=API_KEY)
    assert map.location == '{lat: 0, lng: 0}'


def test_zoomout_on_location_none():
    map = Map(api_key=API_KEY)
    assert map.zoom_start == 1


def test_zoom_set_to_ten_on_init_with_only_location():
    map = Map(api_key=API_KEY, location=(0, 0))
    assert map.zoom_start == 10


def test_set_zoom_start_on_map_initialization():
    zoom_start = 5
    map = Map(api_key=API_KEY, location=(0, 0), zoom_start=zoom_start)
    assert map.zoom_start == zoom_start

    map = Map(api_key=API_KEY, zoom_start=zoom_start)
    assert map.zoom_start == zoom_start
