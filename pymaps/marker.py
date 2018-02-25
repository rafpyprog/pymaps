from .utils import position_to_latLng
from .mapelement import MapElement


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
    NAME = 'marker'
    def __init__(self, position, title='', label='', icon=None, draggable=False,
                 animation=None, opacity=1, optimized=True):
        super().__init__(self.NAME)
        self.map = 'map'
        self.lat, self.lgn = position
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


class MarkerCluster(MapElement):
    '''
    A Marker Clusterer that clusters markers.

    Parameters
    ----------
    * min_cluster_size: int, default 2
        The minimum number of markers to be in a cluster before the markers
        are hidden and a count is shown.

    * grid_size: int, default 60
        The grid size of a cluster in pixels.

    * max_zoom: int, default None
        The maximum zoom level that a marker can be part of a cluster.

    * zoom_on_click: boolean, default True
        Whether the default behaviour of clicking on a cluster is to zoom
        into it.

    * average_center: boolean, default False
        Whether the center of each cluster should be the average of all
        markers in the cluster.
    '''
    NAME = 'marker_cluster'
    def __init__(self, min_cluster_size=2, grid_size=60, max_zoom=None,
                 zoom_on_click=True, average_center=False):
        super().__init__(self.NAME)
        self.map = 'map'
        self.min_cluster_size = min_cluster_size
        self.grid_size = grid_size
        self.set_max_zoom(max_zoom)
        self.zoom_on_click = str(zoom_on_click).lower()
        self.average_center = str(average_center).lower()
        self.grid_size = grid_size

        self.image_path = ('https://raw.githubusercontent.com/googlemaps/'
                           'js-marker-clusterer/gh-pages/images/m')

        self.template = ('''
            {% if children.marker is defined %}
              var markers = [];
              {% for marker in children.marker %}
                {{ marker.html }}
                marker.setMap(null);
                markers.push(marker);
              {% endfor %}
            {% endif %}
            var markerCluster = new MarkerClusterer({{ map }}, markers,
                {imagePath: "{{ image_path }}",
                 zoomOnClick: {{ zoom_on_click }},
                 minimumClusterSize: {{ min_cluster_size }},
                 gridSize: {{ grid_size }},
                 maxZoom: {{ max_zoom }},
                 averageCenter: {{ average_center }},
                });''')

    def set_max_zoom(self, max_zoom):
        if max_zoom:
            self.max_zoom = max_zoom
        else:
            self.max_zoom = 'null'
