def position_to_latLng(position):
    lat, lng = position
    return '{{lat: {}, lng: {}}}'.format(lat, lng)

def jsbool(value):
    return str(value).lower
