'''
    File name: core.py
    Python Version: 3.6
'''

__author__ = "Ricardo Vilela"
__version__ = "0.1"
__email__ = ""
__status__ = "Development"

# Tag das Mensagens:
# [I] -> Informacao
# [A] -> Aviso/Alerta
# [E] -> Erro

import json
from datetime import datetime, timedelta
import os
import sys
import geopandas as gpd
import numpy as np


from geoweather.settings import *
from library import datahub, slackbot

#install sudo apt install libeccodes-tools  

def run_process(filename, filetime, config, info):

    if filename is None:
        filename = datahub.findfile(filetime=filetime, config=config)

    #STEP 1 - read the raster file
    field_variable, field_latitude, field_longitude, field_datetime = datahub.read_netcdf(filename=filename, config=config)

    #STEP 2 - read the geometry file
    gdf = datahub.read_geojson(config=config)

    #step 3 - join procedure
    full_gdf = datahub.spatial_join(raster=field_variable, lat=field_latitude, lon=field_longitude, t=field_datetime, gdf=gdf, config=config)

    #step 4 saving new geojson
    metgdf = datahub.save_geojson(gdf=full_gdf,config=config)
    
    if (metgdf["FIELD"]>0).any():
        print('[INFO] Sending Slack alert')        
        #STEP 5 slack bot message
        slackbot.send_message(config=config, text="[AQPI BOT] Precipitation detected in AQPI domain. Valid for: "+datetime.strftime(field_datetime,"%Y-%m-%d %H:%M"))
    else:
        print('[INFO] Slack alert not necessary')