from shapely.geometry import Point, shape

# Function for fetching quake regions from detail pages
def check_point_in_poly(lat, lng,poly):
    quake_point = Point(float(lng),float(lat))

    # Loop through regions and test
    for zone in poly['features']:
        zone_poly = shape(zone['geometry'])
        if zone_poly.contains(quake_point):
            # We found it! Set zone and stop the loop
            return zone
            break
    # No match found
    return False