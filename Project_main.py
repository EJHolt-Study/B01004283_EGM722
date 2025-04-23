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

#1 Import relevant datasets
    # Northern Ireland Road Network
    # Settlements
    # Counties
    # Satellite raster image

#2  Convert datasets to Geo DataFrames
    # Apply appropriate CRS

#3 Ask the user which 