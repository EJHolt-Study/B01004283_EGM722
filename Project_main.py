# Import support packages
import numpy as np
import rasterio as rio
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches

## Script steps ##

# Importing vector and raster datasets
    # Northern Ireland Road Network
    # Settlements
    # Counties
    # Satellite image / DEM

#2  Convert datasets to Geo DataFrames
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