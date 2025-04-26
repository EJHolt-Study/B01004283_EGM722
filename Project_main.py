# Import support packages
import os
import numpy as np
import rasterio as rio
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches

## Script steps ##

# Importing vector datasets
outline = gpd.read_file(os.path.abspath('data_files/NI_outline.shp')) # Load NI Border Outline - Shapefile(Polygon)
settlements = gpd.read_file(os.path.abspath('data_files/settlements-2015-above-500-threshold.shp')) # Load NI Settlements (pop. over 500) - Shapefile(Polygon)
counties = gpd.read_file(os.path.abspath('data_files/Counties.shp')) # Load NI County Boundaries - Shapefile(Polygon)
roads = gpd.read_file(os.path.abspath('data_files/NI_roads.shp')) # Load NI Road Network - Shapefile(Line)

# Importing and converting 50m DTM raster
DTM_csv = pd.read_csv(os.path.abspath('data_files/OSNI_OpenData_50m_DTM.csv')) # Load CSV of elevation points

print(DTM_csv.min())
# Convert



# Convert datasets to Geo DataFrames
    # Apply appropriate CRS

#3 Ask the user which inputs county and road types they would like to use
    # Split county and road type variables

#4 Perform data processing
    # Select appropriate county
    # Clip Roads, network
    # Don't clip towns

# Mapping
    # Create figure
    # Set map extent
    #