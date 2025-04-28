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
from clip_features import clip_features

## Script steps ##

# Importing vector datasets as GeoDataFrames (GDF)
outline = gpd.read_file(os.path.abspath('data_files/NI_outline.shp')) # Load NI Border Outline - Shapefile(Polygon)
settlements = gpd.read_file(os.path.abspath('data_files/settlements-2015-above-500-threshold.shp')) # Load NI Settlements (pop. over 500) - Shapefile(Polygon)
counties = gpd.read_file(os.path.abspath('data_files/Counties.shp')) # Load NI County Boundaries - Shapefile(Polygon)
roads = gpd.read_file(os.path.abspath('data_files/NI_roads.shp')) # Load NI Road Network - Shapefile(Line)

# Converting GDFs to project CRS (EPSG: 2158)
outline = outline.to_crs(epsg=2158)
settlements = settlements.to_crs(epsg=2158)
counties = counties.to_crs(epsg=2158)
roads = roads.to_crs(epsg=2158)

# REVIEW AT LATER DATE: Importing and converting 50m DTM raster
    # DTM_csv = pd.read_csv(os.path.abspath('data_files/OSNI_OpenData_50m_DTM.csv')) # Load CSV of elevation points

# Creating user prompt step to select a specific county
counties['CountyName'] = counties['CountyName'].str.title() # Convert values in 'CountyNames' column to Title Case
print('Select county for map extent:') # Add initial text
print('') # Add line break
print('All') # Print 'All' input option
print(counties['CountyName'].to_string(index=False)) # Prints County Names with index removed
print('') # Add line break
selection = (input('Input county name here:')) # Create user input parameter step

select_edited = selection.title() # Converting input to title case
test_county = select_edited in counties['CountyName'].unique() # Bool check if selection is a valid county name
test_all = select_edited == 'All' # Bool check all counties has been selected

while (test_county is False) and (test_all is False): # Check whether a valid input has been provided

    # When an invalid input is provided
    selection = (input('Please provide a correct input:')) # Request new input from user
    # Re-run checks on new input
    select_edited = selection.title()
    test_county = select_edited in counties['CountyName'].unique()
    test_all = select_edited == 'All'

# Creating specified map based on selection
if select_edited in counties['CountyName'].unique(): # Check if selection is a specific county
    # Clipping counties GDF to selected area
    map_counties = counties.loc[counties['CountyName']==select_edited] # Creates GDF of clipped county layer

    # Clipping additional GDFs to extent of selected area, using clip_features function
    map_roads = clip_features(roads,map_counties)
    map_settlements = clip_features(settlements,map_counties)

    print('Thank you for selecting County: ',select_edited)
    print(map_counties.head())
    print(map_settlements.head())

elif select_edited == 'All': # Check if all counties have been selected

    print('Thank you for selecting all counties')

    # Clip Roads, network


# Mapping
    # Create figure
    # Set map extent
