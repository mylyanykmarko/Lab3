import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py


def get_data(acct):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    #Changes start here

    print('')
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '10'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    headers = dict(connection.getheaders())

    #Here I searching friends and their locations

    names = []
    locations = []
    for u in js['users']:
        names.append((u['screen_name']))
        locations.append(u['location'])
        if 'status' not in u:
            continue
        s = u['status']['text']

    return names, locations


def createmap(name, place):
    """
    list, list -> None
    this function uses geopy to find cordinates and mark it on map
    also this function creates map

    """
    map = folium.Map(zoom_start=4, tiles="Mapbox bright")
    geolocator = Nominatim()

    feature_group = folium.FeatureGroup("Locations")

    for i in range(len(name)):
        if place[i] != "":
            location = geolocator.geocode(place[i])
            lat = location.latitude
            lng = location.longitude
            new = folium.Marker(location=[lat, lng], popup=name[i])
            feature_group.add_child(new)

    map.add_child(feature_group)
    map.save("static/Friends.html")


