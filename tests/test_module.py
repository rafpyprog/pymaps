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
