import jinja2

from .utils import position_to_latLng


class Marker():
    '''A marker identifies a location on a map. By default, a marker uses a
    standard image. Markers can display custom images using the icon
    parameter.'''
    def __init__(self, position):
        self._map = 'map'
        self.position = position_to_latLng(position)
        pass
