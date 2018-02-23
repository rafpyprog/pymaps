import base64
import glob
import json
from operator import itemgetter
import os

from jinja2 import Environment, FileSystemLoader
from css_html_js_minify.js_minifier import js_minify_keep_comments

from .utils import position_to_latLng
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


def load_style(stylename):
    STYLES_DIR = os.path.join(this_dir, 'styles')
    stylefile = os.path.join(STYLES_DIR, stylename + '.txt')
    with open(stylefile) as f:
        style = f.read()
    return style


class FitBounds(MapElement):
    ''' Sets the viewport to contain the given bounds, using a rectangle
    from the points at its south-west and north-east corners.

    Parameters
    ----------
    * bounds: list or tuple of geografical coordinates (lat, long)
    '''
    def __init__(self, coordinates):
        super().__init__('fitbounds')
        self.coordinates = coordinates
        self.sw, self.ne = self.calc_bounds(self.coordinates)
        self.template = (''' var bounds = new google.maps.LatLngBounds(
                               {{ sw }}, {{ ne }});
                             map.fitBounds(bounds);''')

    def calc_bounds(self, coordinates):
        if len(coordinates) == 1:
            return coordinates[0], coordinates[0]

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
    * location
    * map_type
    * style
    * width
    * height
    * zoom_start
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

    def __init__(self, location=None, map_type='roadmap', style=None,
                 width='100%', height='500px', zoom_start=None, show_pegman=True,
                 show_zoom_control=True, disable_default_ui=False,
                 title=None, api_key=""):
        self.template_file = TEMPLATE

        if location is None:
            # If location is not passed we center and zoom out.
            self.initial_location_is_set = False
            self.location = position_to_latLng([0, 0])
            self.zoom_start = zoom_start or 1
        else:
            self.location = position_to_latLng(location)
            self.zoom_start = zoom_start or 10

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
        self.children = {}

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
        # If the map was created without an initial location and it has any
        # child markers, use the markers as location to center the map.
        map_has_markers = 'marker' in self.children
        if self.initial_location_is_set is False and map_has_markers:
            markers = self.children['marker']
            if len(markers) == 1:
                lat, lgn = markers[0].lat, markers[0].lgn
                self.location = position_to_latLng([lat, lgn])
            else:
                coordinates = [(i.lat, i.lgn) for i in markers]
                self.fit_bounds(coordinates)

        html = render(self.template_file, self.__dict__)
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
