from operator import add

from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
from jsbeautifier import beautify
import pandas as pd


def info_window(values):
    data = ''.join([f'<dt>{k}</dt><dd>{v}</dd>' for k, v in values.items()])
    return f'<dl>{data}</dl>'


class LatLng(str):
    ''' A LatLng is a point in geographical coordinates: latitude and
        longitude. '''
    def __new__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        return str.__new__(self, f'{{lat: {lat}, lng: {lng}}}')


class Marker(str):
    ''' A marker identifies a location on a map.
     Parameters:
    * location (tuple or list, default None) – Latitude and Longitude of Map (Northing, Easting).
    '''
    def __new__(self, location=None, icon=None, title='', gmap='map', info_window=None):

        self.attributes = {}
        self.attributes['position'] = LatLng(*position)
        self.attributes['map'] = gmap

        if title != '':
            self.attributes['title'] = f'"{title}"'

        if icon is not None:
            self.attributes['icon'] = f'"{icon}"'

        self.template = self.fill_template(self.attributes)
        self.template = self.add_info_window(info_window, self.template)

        return str.__new__(self, self.template)

    def fill_template(attr):
        template = 'var marker = new google.maps.Marker({{{}}}); @infowindow'
        args = ',\n        '.join([f'{k}: {v}' for k, v in attr.items()])
        return template.format(args)

    def add_info_window(info_window, template):
        if info_window is not None:
            func = f'attachInfoWindow(marker, "{info_window}");'
            return template.replace('@infowindow', func)
        return template.replace('@infowindow', '')

    def __repr__(self):
        return beautify(self.template)

    def __str__(self):
        return beautify(self.template)


class Map():
    def __init__(self, api_key, markers, map_type='roadmap', height='250px', width='100%', zoom=4, icon=None, labels=None,
                 title='', info_windows=None, show_zoomcontrol=True, show_pegman=True):
        self.template = open('template.html').read()
        self.api_key = api_key
        self.map_type = map_type
        self.height = height
        self.width = width
        self.zoom = zoom
        self.markers = markers
        self.add_markers(self.markers, icon=icon, labels=labels, info_windows=info_windows)
        self.title = title
        self.show_pegman = show_pegman
        self.show_zoomcontrol = show_zoomcontrol

    def add_markers(self, markers, icon=None, labels=None, info_windows=None):
        if isinstance(markers, pd.core.frame.DataFrame):
            for n, pos in enumerate(markers.itertuples(index=False)):
                label = ''
                info = None
                if labels is not None:
                    label = labels[n]

                if info_windows is not None:
                    info = info_windows[n]

                marker = Marker(pos, icon=icon, title=label, info_window=info)

                self.template = self.template.replace('@marker', f'{marker}\n@marker')

    @property
    def center(self):
        if isinstance(self.markers, pd.core.frame.DataFrame):
            return LatLng(*self.markers.mean())
        elif isinstance(self.markers[0], (float, int)):
            center = self.markers
        else:
            if len(self.markers) > 1:
                center = [sum(i) / len(self.markers)
                          for i in [i for i in zip(*self.markers)]]
            else:
                center = self.markers[0]
        return LatLng(*center)

    @property
    def html(self):
        html = self.template.replace('@marker', '')
        html = html.replace('@api_key', self.api_key)
        html = html.replace('@map_height', self.height)
        html = html.replace('@map_width', self.width)
        html = html.replace('@map_center', self.center)
        html = html.replace('@map_zoom', str(self.zoom))
        html = html.replace('@map_type', f'"{self.map_type}"')
        html = html.replace('@title', str(self.title))
        html = html.replace('@map_showpegman', str(self.show_pegman).lower())
        assert isinstance(self.show_zoomcontrol, bool)
        html = html.replace('@map_showzoomcontrol', str(self.show_zoomcontrol).lower())
        return html

    def show(self):
        return display(HTML(self.html))

    def __repr__(self):
        return BeautifulSoup(self.html, 'html.parser').prettify()
