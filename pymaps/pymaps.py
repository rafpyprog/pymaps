import base64
import glob
import json
from operator import itemgetter
import os

from jinja2 import Environment, FileSystemLoader
from css_html_js_minify.js_minifier import js_minify_keep_comments

from .marker import Marker, MarkerCluster
from .utils import position_to_latLng, calc_avg_position
from .mapelement import MapElement


this_dir, _ = os.path.split(__file__)
TEMPLATE_DIR = 'templates'
TEMPLATE_FILE = 'template.j2'
TEMPLATE = os.path.join(this_dir, TEMPLATE_DIR, TEMPLATE_FILE)


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    loader = FileSystemLoader(path or './')
    env = Environment(loader=loader)
    html = env.get_template(filename).render(context)
    return html


class FitBounds(MapElement):
    ''' Sets the viewport to contain the given bounds, using a rectangle
    from the points at its south-west and north-east corners.

    Parameters
    ----------
    * bounds: list or tuple of geografical coordinates (lat, long)
    '''
    NAME = 'fitbounds'
    def __init__(self, coordinates):
        super().__init__(self.NAME)
        self.coordinates = coordinates
        self.sw, self.ne = self.calc_bounds(self.coordinates)
        self.template = (''' var bounds = new google.maps.LatLngBounds(
                               {{ sw }}, {{ ne }});
                             map.fitBounds(bounds);''')

    def calc_bounds(self, coordinates):
        if not all(isinstance(i, (tuple, list)) for i in coordinates):
            sw = ne = position_to_latLng(coordinates)
        else:
            min_lat = min(coord[0] for coord in coordinates)
            max_lat = max(coord[0] for coord in coordinates)

            min_lgn = min(coord[1] for coord in coordinates)
            max_lgn = max(coord[1] for coord in coordinates)

            sw = position_to_latLng([min_lat, min_lgn])
            ne = position_to_latLng([max_lat, max_lgn])
        return sw, ne


class Map():
    '''Create a Map with Google Maps Javascript API

    Parameters
    ----------
    * center
    * map_type
    * style
    * width
    * height
    * zoom
    * show_pegman
    * show_zoom_control
    * disable_default_ui
    * title
    * minify
    * api_key

    Returns
    -------
    pyGmaps Map Object

    Examples
    --------
    '''

    def __init__(self, center=None, map_type='roadmap', style=None,
                 width='100%', height='500px', zoom=None, show_pegman=True,
                 show_zoom_control=True, disable_default_ui=False,
                 title=None, api_key=""):

        self.children = {}
        self.center = center
        self.zoom = zoom

        self.template_file = TEMPLATE
        self.map_type = map_type

        if style is not None:
            self.set_style(style)
        else:
            self.style = style

        self.width = width
        self.height = height

        if api_key == '':
            raise ValueError('Missing Google Maps API key.')
        else:
            self.api_key = api_key

        self.show_pegman = int(show_pegman)
        self.show_zoom_control = int(show_zoom_control)
        self.disable_default_ui = int(disable_default_ui)
        self.title = title

    @property
    def has_marker(self):
        return Marker.NAME in self.children

    @property
    def has_cluster(self):
        return MarkerCluster.NAME in self.children

    @property
    def markers(self):
        marks = []
        markers = self.children.get(Marker.NAME, None)
        clusters = self.children.get(MarkerCluster.NAME, None)
        if markers:
            latlng = [(i.lat, i.lgn) for i in markers]
            marks.extend(latlng)
        if clusters:
            for cluster in clusters:
                markers = cluster.children.get('marker', None)
                latlng = [(i.lat, i.lgn) for i in markers]
                if markers:
                    marks.extend(latlng)
        return marks

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        if value is not None:
            self._center = position_to_latLng(value)
        else:
            self._center = None

    def fit_bounds(self, coordinates):
        bounds = FitBounds(coordinates)
        self.add_child(bounds)

    def set_style(self, style):
        '''
        Set map style using the built-in styles or a custom style.
        More about styling at:
        https://developers.google.com/maps/documentation/javascript/styling

        Parameters
        ----------
        * style: str, {'aubergine', 'dark', 'grayscale', 'night', 'old',
            'redberry', 'retro', 'silver', 'water', 'wine'}, or valid JSON
            string.
        '''
        STYLES_DIR = os.path.join(this_dir, 'styles')

        is_built_in = glob.glob(os.path.join(STYLES_DIR, style + '.txt')) != []
        if is_built_in:
            style_file = os.path.join(STYLES_DIR, style + '.txt')
            with open(style_file) as f:
                style_config = f.read()
            self.style = style_config
        else:
            try:
                json.loads(style)
            except json.JSONDecodeError:
                raise json.JSONDecoder('Style must be a valid JSON.')
            else:
                self.style = style

    def _html(self):
        # ensure map has a center setted
        if self.center is None:
            if any([self.has_marker, self.has_cluster]):
                avg_position = calc_avg_position(self.markers)
                self.center = avg_position
            else:
                self.center = (0, 0)

        # if zoom is none zoom out and or close up if just one marker
        if self.zoom is None:
            if self.markers == [] or len(self.markers) > 1:
                self.zoom = 2
            else:
                self.zoom = 14

        self.context = self.__dict__
        self.context['center'] = self.center
        self.context['zoom'] = self.zoom

        html = render(self.template_file, self.context)
        return html

    @property
    def html(self):
        return self._html()

    def add_child(self, child):
        name = child.element_name
        if self.children.get(name, False):
            self.children[name].append(child)
        else:
            self.children[name] = []
            self.children[name].append(child)

    def _repr_html_(self):
        '''Displays the Map in a Jupyter notebook'''
        HTML = ("data:text/html;charset=utf-8;base64," +
                base64.b64encode(self.html.encode('utf8')).decode('utf8'))
        iframe = ('<iframe src="{}" style="height:{};width:{};border:none !important">'
                  '</iframe>')
        return iframe.format(HTML, self.height, self.width)
