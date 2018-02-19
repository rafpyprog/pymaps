from jinja2 import Template

from .utils import position_to_latLng


class MapElement():
    def __init__(self, element_name):
        self.element_name = element_name
        self.template = ''

    def render(self):
        context = self.__dict__.copy()
        context.pop('element_name')
        context.pop('template')
        return Template(self.template).render(**context)

    @property
    def html(self):
        return self.render()

    def add_to(self, map):
        placeholder = '// >>{}'.format(self.element_name)
        map.html = map.html.replace(placeholder, self.html + '\n' + placeholder)


class Marker(MapElement):
    '''A marker identifies a location on a map. By default, a marker uses a
    standard image. Markers can display custom images using the icon
    parameter.

    Parameters
    ----------

    * position
    * title
    * draggable
    * animation: DROP, BOUNCE
    '''

    def __init__(self, position, title='', label='', icon=None, draggable=False,
                 animation=None, opacity=0, optimized=True):
        super().__init__('marker')
        self.map = 'map'
        self.position = position_to_latLng(position)
        self.title = title
        self.label = label
        self.icon = icon
        self.draggable = str(draggable).lower()
        if animation is not None:
            self.animation = 'google.maps.Animation.' + animation
        else:
            self.animation = 'null'
        self.opacity = opacity
        self.optimized = str(optimized).lower()

        self.template = ('''
            var marker = new google.maps.Marker({
              position: {{ position }},
              draggable: {{ draggable }},
              map: {{ map }},
              title: "{{ title }}",
              label: "{{ label }}",
              animation: {{ animation }},
              {% if icon is none %}
                icon: null,
              {% else %}
                icon: "{{ icon }}",
              {% endif %}
              opacity: {{ opacity }},
              optimized: {{ optimized }}
            });''')
