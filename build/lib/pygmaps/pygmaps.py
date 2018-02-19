import base64
import json
import os

from jinja2 import Environment, FileSystemLoader

this_dir, _ = os.path.split(__file__)
TEMPLATE_DIR = 'templates'
TEMPLATE_FILE = 'template.j2'
TEMPLATE = os.path.join(this_dir, TEMPLATE_DIR, TEMPLATE_FILE)


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    loader = FileSystemLoader(path or './')
    env = Environment(loader=loader)
    return env.get_template(filename).render(context)


def position_to_latLng(position):
    lat, lng = position
    return '{{lat: {}, lng: {}}}'.format(lat, lng)


def load_style(stylename):
    STYLES_DIR = os.path.join(this_dir, 'styles')
    stylefile = os.path.join(STYLES_DIR, stylename + '.txt')
    with open(stylefile) as f:
        style = f.read()
    return style


class Map():
    '''Create a Map with Google Maps Javascript API

    Returns
    -------
    pyGmaps Map Object

    Examples
    --------
    '''

    def __init__(self, location=None, map_type='roadmap', style=None,
                 width='100%',
                 height='500px', zoom_start=10, show_pegman=True,
                 show_zoom_control=True, disable_default_ui=False,
                 title=None, api_key=""):
        self.template_file = TEMPLATE
        if not location:
            # If location is not passed we center and zoom out.
            self.location = position_to_latLng([0, 0])
            self.zoom_start = 1
        else:
            self.location = position_to_latLng(location)
            self.zoom_start = zoom_start
        self.map_type = map_type
        if style:
            self.style = load_style(style)
        else:
            self.style = style
        self.width = width
        self.height = height
        self.api_key = api_key
        self.show_pegman = int(show_pegman)
        self.show_zoom_control = int(show_zoom_control)
        self.disable_default_ui = int(disable_default_ui)
        self.title = title
        self.html = render(self.template_file, self.__dict__)

    def _repr_html_(self):
        '''Displays the Map in a Jupyter notebook'''
        html = self.html
        return html
