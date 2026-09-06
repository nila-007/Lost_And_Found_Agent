from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two locations in meters.
    """

    earth_radius = 6371000  # meters

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    difference_lat = radians(lat2 - lat1)
    difference_lon = radians(lon2 - lon1)

    a = (
        sin(difference_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(difference_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c

    return round(distance, 2)