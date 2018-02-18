import base64
import json
import os

from jinja2 import Environment, FileSystemLoader


TEMPLATE = '/home/rafael/Documentos/Projetos/pyGmaps/templates/template.j2'


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    loader = FileSystemLoader(path or './')
    env = Environment(loader=loader)
    return env.get_template(filename).render(context)


def position_to_latLng(position):
    lat, lng = position
    return '{{lat: {}, lng: {}}}'.format(lat, lng)

def load_style()


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
