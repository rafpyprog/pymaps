import os
from pathlib import Path
import pytest

from pymaps import Map
from pymaps.marker import Marker, MarkerCluster
from pymaps.utils import position_to_latLng, calc_avg_position


API_KEY = os.environ['MAPS_API_KEY']


def test_calc_avg_position():
    coordinates = [(10, 10), (40, 40), (10, 10)]
    avg = calc_avg_position(coordinates)
    assert avg == (20., 20.)


def test_calc_avg_position_raise_value_error():
    coordinates = (10, 10)
    with pytest.raises(ValueError):
        avg = calc_avg_position(coordinates)


def test_position_to_latLng():
    position = (10, -10)
    latlng = position_to_latLng(position)
    assert latlng == '{lat: 10, lng: -10}'


def test_instanciate_map():
    map = Map(api_key=API_KEY)
    assert isinstance(map, Map)


def test_map_raise_valueerror_without_api_key():
    with pytest.raises(ValueError):
        map = Map()


def test_map_center_to_zero_without_markers():
    map = Map(api_key=API_KEY)
    map.html
    assert map.center == '{lat: 0, lng: 0}'


def test_map_center_parameter_set_center():
    map = Map(api_key=API_KEY, center=(20, 20))
    map.html
    assert map.center == '{lat: 20, lng: 20}'


def test_add_marker_to_map():
    map = Map(api_key=API_KEY, center=(20, 20))
    markers = [(10, 10), (20, 20)]
    [Marker(i).add_to(map) for i in markers]
    assert isinstance(map.children[Marker.NAME], list)
    assert len(map.children[Marker.NAME]) == len(markers)


def test_map_center_average_markers_position():
    map = Map(api_key=API_KEY)
    markers = [(10, 10), (20, 20)]
    for i in markers:
        Marker(i).add_to(map)
    map.html
    assert map.center == '{lat: 15.0, lng: 15.0}'


def test_map_center_average_cluster_markers_position():
    map = Map(api_key=API_KEY)
    markers = [(10, 10), (20, 20)]
    cluster = MarkerCluster()
    for i in markers:
        Marker(i).add_to(cluster)
    cluster.add_to(map)
    map.html
    assert map.center == '{lat: 15.0, lng: 15.0}'


def test_map_center_average_cluster_markers_and_markers_position():
    map = Map(api_key=API_KEY)
    markers = [(10, 10), (20, 20)]
    cluster = MarkerCluster()
    for i in markers:
        Marker(i).add_to(cluster)
    cluster.add_to(map)
    Marker([10, 10]).add_to(map)
    map.html
    assert map.center == '{lat: 13.333333, lng: 13.333333}'


def test_set_center():
    map = Map(api_key=API_KEY)
    map.center = (10, 10)
    assert map.center == '{lat: 10, lng: 10}'


def test_zoom_none_set_1_withoutmarkers():
    map = Map(api_key=API_KEY)
    map.html
    assert map.zoom == 2


def test_zoom_none_set_value():
    map = Map(api_key=API_KEY, zoom=14)
    map.html
    assert map.zoom == 14


def test_zoom_none_fitbounds():
    map = Map(api_key=API_KEY)
    markers = [(10, 10), (20, 20)]
    for i in markers:
        Marker(i).add_to(map)
    map.html
    assert map.zoom == 2


def test_set_map_builtin_style():
    map = Map(api_key=API_KEY)
    stylename = 'aubergine'
    map.set_style(stylename)

    this_dir, _ = os.path.split(__file__)
    root_dir = os.path.dirname(this_dir)
    stylefile = os.path.join(root_dir, 'pymaps', 'styles', stylename + '.txt')

    with open(stylefile) as f:
        style_config = f.read()

    assert map.style == style_config
