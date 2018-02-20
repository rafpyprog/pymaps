from .utils import position_to_latLng
from .mapelement import MapElement


class MarkerCluster(MapElement):
    COLORS = ['blue', 'yellow', 'red', 'pink', 'purple']
    def __init__(self, color='yellow'):
        super().__init__('marker_cluster')
        self.map = 'map'
        self.color = color
        image_url = ('https://raw.githubusercontent.com/googlemaps/'
                     'v3-utility-library/master/markerclusterer/'
                     'images/m{}.png').format
        self.image_path = image_url(COLORS.index(self.color) + 1)        
        self.template = ('''
            var markerCluster = new MarkerClusterer({{ map }}, {{ markers }},
                {imagePath: '{{ image_path }}'});''')

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
                 animation=None, opacity=1, optimized=True):
        super().__init__('marker')
        self.map = 'map'
        self.position = position_to_latLng(position)
        self.title = title
        self.label = label
        self.icon = icon
        self.draggable = str(draggable).lower()
        self.set_animation(animation)
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

    def set_animation(self, animation=None):
        '''
        Specify the way a marker is animated.

        * DROP indicates that the marker should drop from the top of the
          map to its final location when first placed on the map. Animation
          will cease once the marker comes to rest and animation will
          revert to null.

        * BOUNCE indicates that the marker should bounce in place. A bouncing
          marker will continue bouncing until its animation property is
          explicitly set to null.

        Parameters
        ----------
        * animation : {'BOUNCE', 'DROP', None}, default None
        '''
        if animation is None:
            self.animation = 'null'
        else:
            self.animation = 'google.maps.Animation.' + animation

    def remove_animation(self):
        self.animation = 'null'
