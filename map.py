import folium
import pandas


json = pandas.read_json('volcanoes.json')
data = json['properties']
lon = []
lat = []
elev = []
name = []
for d in data:
    lon.append(d['LON'])
    lat.append(d['LAT'])
    elev.append(d['ELEV'])
    name.append(d['NAME_'])


def set_color(elev):
    if elev < 0:
        return 'blue'
    elif 0 <= elev < 1000:
        return 'green'
    elif 1000 <= elev < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.09], zoom_start=4, tiles='Mapbox Bright')

# Volcanoes layer (feature group)
fg_vol = folium.FeatureGroup(name='Volcanoes')
for lt, ln, el, n in zip(lat, lon, elev, name):
    if n == 'UNNAMED':
        n = ''
    label = n+" ("+str(el)+"m)"
    popup = folium.Popup(label, parse_html=True)
    fg_vol.add_child(folium.CircleMarker(location=[lt,ln], radius= 8, popup=popup,
                                     fill_color=set_color(el), color='grey', fill=True,
                                     fill_opacity=0.9))

# Population layer (feature group)
fg_pop = folium.FeatureGroup(name='Population')
geo_data = open('world.json','r', encoding='utf-8-sig').read()
fg_pop.add_child(folium.GeoJson(geo_data, style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 10000000
                                                                else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                                else 'red'}))


# add fg to map
map.add_child(fg_pop)
map.add_child(fg_vol)

map.add_child(folium.LayerControl())
map.save('map.html')

