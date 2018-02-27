from operator import itemgetter

import numpy as np


def position_to_latLng(position):
    lat, lng = position
    return '{{lat: {}, lng: {}}}'.format(lat, lng)


def calc_avg_position(coordinates):
    '''
    Calculate the average position of a list of lat, long coordinates.

    Parameters
    ----------
    * coordinates: list or tuple
        List of (lat, lng) coordinates.

    Returns
    -------
        tuple
     '''
    if not all(isinstance(i, (list, tuple)) for i in coordinates):
        error = 'Coordinates is not an iterable of [lat, lng] or (lat, lng)'
        raise ValueError(error)

    n_coordinates = len(coordinates)
    avg_lat = sum(i[0] for i in coordinates) / n_coordinates
    avg_lng = sum(i[1] for i in coordinates) / n_coordinates

    avg_position = (round(avg_lat, 6), round(avg_lng, 6))
    return avg_position


def random_latlng():
    ''' Returns a random lat, lng tuple ''' 
    lat = np.random.uniform(low=-85.0, high=85.01)
    lat = [min(85.0, lat) if lat > 85.0 else lat][0]

    lng = np.random.uniform(low=-180.0, high=180.01)
    lng = [min(180, lng) if lng > 180. else lng][0]
    return round(lat, 6), round(lng, 6)
