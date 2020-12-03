import json

import geopandas as gpd
import pandas as pd
import plotly.express as px

def duplicate_rows(df, target='Year'):
    """
    `target` should be an integer column of `df`
    """
    partials = {y: df[df[target] <= y].copy() for y in df[target].unique()}
    for key in partials:
        partials[key][target] = key
    return pd.concat(partials)

shp_path = '/home/james/Projects/annexation/shapefile'
ll_crs = 'epsg:4326'
rva_lat = 37.54129
rva_lon = -77.434769

gdf = gpd.read_file(shp_path)
gdf = gdf.to_crs(ll_crs)
gdf['shape_id'] = range(len(gdf)) # need a unique identifier for each shape
gdf['Year'] = gdf['Year'].astype(int)
gdf = gdf.sort_values(by='Year')
gdf = duplicate_rows(gdf)
geojson = json.loads(gdf.to_crs(ll_crs).to_json())

# might have to manually build the frames individually?
# https://community.plotly.com/t/cumulative-lines-animation-in-python/25707
# fig.frames.data[0].z maybe is the list of years to show?
# copying the row and changing the year can keep it shown every animation
# seems redundant & also means every shape is same color
# when change color to `shape_id` column this last issue is sorted
# just need to write something to duplicate all that information


fig = px.choropleth_mapbox(gdf, geojson=geojson, color="shape_id",
                                                      locations="shape_id", featureidkey="properties.shape_id",
                                                      center = {"lat": rva_lat, "lon": rva_lon},
                                                      mapbox_style="carto-positron", zoom=11, animation_frame='Year')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()