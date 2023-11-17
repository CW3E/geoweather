from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num, date2index
import numpy as np
import re
import gzip
import os
import xarray as xr
import pandas as pd
import geopandas as gpd
from geoweather.settings import *

def findfile(filetime, config):
    
    #filetime = filetime.replace(second=59)
    
    print('[INFO] Downloading MRMS product')

    

    file_list = []
    timelist = pd.date_range(start=filetime-timedelta(hours=2),end=filetime,freq="1min")
    for checking_time in timelist:
        if os.path.isfile(config["raster_field"]["filename"].format(procdate=checking_time)):
            file_list.append(config["raster_field"]["filename"].format(procdate=checking_time))
    
    if file_list == []:
        print('[ERROR] Raster file not found')
        exit()
    
    latest_file = np.sort(file_list)[-1]

    return latest_file

def read_netcdf(filename, config):
    print('[INFO] reading ',filename)

    nc = Dataset(filename)

    field_latitude = nc.variables[config["raster_field"]["yvar"]["name"]][:]
    field_longitude = nc.variables[config["raster_field"]["xvar"]["name"]][:]
    field_variable = nc.variables[config["raster_field"]["fieldvar"]["name"]][:][:]
    field_datetime = nc.variables[config["raster_field"]["tvar"]["name"]]

    field_datetime = num2date(times=field_datetime[:],units=field_datetime.units, only_use_cftime_datetimes=False, only_use_python_datetimes=True)[0]
    

    return field_variable, field_latitude, field_longitude, field_datetime


def read_geojson(config):
    
    geojson_filename = config["geometry_field"]["filename"]
    print('[INFO] reading ',geojson_filename)

    gdf = gpd.read_file(geojson_filename)
    
    return gdf

def spatial_join(raster,lat, lon, t, gdf, config):
    print('[INFO] performing the spatial join between the raster and the geometry datasets')
    rlon,rlat = np.meshgrid(lon,lat)
    
    rlon = rlon.flatten()
    rlat = rlat.flatten()
    raster = raster.flatten()

    field_gdf = pd.DataFrame(data={"lat":rlat,"lon":rlon,"FIELD":raster})
    
    field_gdf = gpd.GeoDataFrame(field_gdf, geometry=gpd.points_from_xy(field_gdf.lon, field_gdf.lat), crs="EPSG:4326")


    joint_df = gpd.sjoin(left_df=gdf, right_df=field_gdf, how='left', predicate='intersects', lsuffix='left', rsuffix='right')
    if config["output"]["spatial_agg"]=="max": 
        var_by_geometry = pd.DataFrame(joint_df.groupby(['HUC10'])['FIELD'].max())
    elif config["output"]["spatial_agg"]=="mean":
        var_by_geometry = pd.DataFrame(joint_df.groupby(['HUC10'])['FIELD'].mean())
    elif config["output"]["spatial_agg"]=="sum":
        var_by_geometry = pd.DataFrame(joint_df.groupby(['HUC10'])['FIELD'].sum())
    else:
        print('[ERROR] unknow spatial_agg parameter: ',config["ouptut"]["spatial_agg"]+'.','The valid options are: min, max or mean')
        exit()


    full_gdf = gpd.GeoDataFrame(var_by_geometry.merge(gdf, on = ["HUC10"]))
    full_gdf['DATETIME'] = [datetime.strftime(t,'%Y-%m-%d %H:%M')]*len(gdf)
 
    return full_gdf

    
def save_geojson(gdf,config):
    gdf.to_file(config["output"]["filename"], driver="GeoJSON")
    line_prepender(config["output"]["filename"],config["output"]["js_varname"]+" =")
    print('[INFO] file saved: ',config["output"]["filename"])
    return gdf


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
