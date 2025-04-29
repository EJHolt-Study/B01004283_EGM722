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
from data_processing import clip_features
from data_processing import roads_symbology

## Setup project datasets ##
#-----------------------------------------------------------------------------------------------------------------------
# Importing vector datasets as GeoDataFrames (GDF)
outline = gpd.read_file(os.path.abspath('data_files/NI_outline.shp')) # load NI Border Outline - Shapefile(Polygon)
settlements = gpd.read_file(os.path.abspath('data_files/settlements-2015-above-500-threshold.shp')) # load NI Settlements (pop. over 500) - Shapefile(Polygon)
counties = gpd.read_file(os.path.abspath('data_files/Counties.shp')) # load NI County Boundaries - Shapefile(Polygon)
roads = gpd.read_file(os.path.abspath('data_files/NI_roads.shp')) # load NI Road Network - Shapefile(Line)

# Converting GDFs to project CRS (EPSG: 2158)
outline = outline.to_crs(epsg=2158)
settlements = settlements.to_crs(epsg=2158)
counties = counties.to_crs(epsg=2158)
roads = roads.to_crs(epsg=2158)

# REVIEW AT LATER DATE: Importing and converting 50m DTM raster
    # DTM_csv = pd.read_csv(os.path.abspath('data_files/OSNI_OpenData_50m_DTM.csv')) # Load CSV of elevation points

## Initial user input step to select map extent ##
#-----------------------------------------------------------------------------------------------------------------------
# Creating user prompt step to select a specific county
counties['CountyName'] = counties['CountyName'].str.title() # convert values in 'CountyNames' column to Title Case
print('Select county for map extent:') # add initial text
print('') # add line break
print('All') # print 'All' input option
print(counties['CountyName'].to_string(index=False)) # prints County Names with index removed
print('') # add line break


selection = (input('Input county name here:')) # create user input parameter step

select_edited = selection.title() # converting input to title case
test_county = select_edited in counties['CountyName'].unique() # bool check if selection is a valid county name
test_all = select_edited == 'All' # bool check all counties has been selected

while (test_county is False) and (test_all is False): # check whether a valid input has been provided

    # When an invalid input is provided
    selection = (input('Please provide a correct input:')) # request new input from user
    # Re-run checks on new input
    select_edited = selection.title()
    test_county = select_edited in counties['CountyName'].unique()
    test_all = select_edited == 'All'

# Creating specified map based on selection
if select_edited in counties['CountyName'].unique(): # check if selection is a specific county
    # Clipping counties GDF to selected area
    map_counties = counties.loc[counties['CountyName']==select_edited] # creates GDF of clipped county layer

    # Confirm to selection to user and confirm the map is being generated
    print('Thank you for selecting County: ',select_edited) # confirm user selection
    print('Generating map') # Provide status update

    # Clipping additional GDFs to extent of selected area, using clip_features function
    map_roads = clip_features(roads, map_counties) # creating clipped road network GDF
    map_settlements = clip_features(settlements,map_counties) # creating GDF for settlements in selected county

elif select_edited == 'All': # check if all counties have been selected
    print('Thank you for selecting all counties') # confirm user selection
    print('Generating map') # provide status update

    # Create GDF of all counties combined
    map_counties = counties.dissolve() # dissolving counties into single Multi-polygon geometry

    # Clipping additional GDFs to extent of NI border, to remove overlaps
    map_roads = roads # clipping road network GDF to extent of NI border
    map_settlements = settlements # clipping settlements GDF to extent of NI border

## Generating map features ##
#-----------------------------------------------------------------------------------------------------------------------
# Create figure and map axis
proj_crs = ccrs.UTM(29) # create copy of project crs (EPSG: 2158 - UTM zone 29)
figure = plt.figure(figsize=(10,10)) # creating 10" by 10" figure
axes = plt.axes(projection=proj_crs) # create the map axes on the figure with project crs

# Set map extent
minx,miny,maxx,maxy = map_counties.total_bounds # create map extent variables using selected area
axes.set_extent([minx,maxx,miny,maxy],crs=proj_crs) # setting axes extent to variables, using project crs

# Adding map features
map_counties = ShapelyFeature(counties['geometry'],proj_crs,edgecolor='k',facecolor='none') # defining county details...
#... with red edge-color and gXXXXX face-color
axes.add_feature(map_counties) # Add county layer to map axes

print(type(map_counties))

# Separating road GDF into the primary road types
roads_motorways = map_roads[map_roads['Road_class']=='MOTORWAY'] # extracting all motorway road sections
roads_dualcarr = map_roads[map_roads['Road_class']=='DUAL_CARR'] # extracting all dual-carriageway road sections
roads_aclass = map_roads[map_roads['Road_class']=='A_CLASS'] # extracting all A-road sections
roads_bclass = map_roads[map_roads['Road_class']=='B_CLASS'] # extracting all B-road sections
# Grouping remaining minor road types
roads_minor = map_roads[map_roads['Road_class'].isin(['<4M_TARRED','<4M_T_OVER','CL_MINOR','CL_M_OVER'])] # extracting all minor road sections


# Generate road features and symbology for map plot, using roads_symbology function
roads_motorways = roads_symbology(roads_motorways,'motorway') # apply motorway symbology
roads_dualcarr = roads_symbology(roads_dualcarr,'dualcarr') # apply dual-carriageway symbology
roads_aclass = roads_symbology(roads_aclass,'aclass') # apply A-road symbology
roads_bclass = roads_symbology(roads_bclass,'bclass') # apply B-road symbology
roads_minor = roads_symbology(roads_minor,'minor') # apply minor road symbology

# Add road features
axes.add_feature(roads_motorways) # add motorways to map
axes.add_feature(roads_dualcarr) # add dual-carriageways to map
axes.add_feature(roads_aclass) # add A-roads to map
axes.add_feature(roads_bclass) # add B-roads to map
axes.add_feature(roads_minor) # add minor roads to map



# Plotting the map
plt.show() # show map figure in pop-out window

# Saving map plot
save = input('Would you like to save the map (Y/N): ') # new user input parameter to select if map should be saved
choice1 = save == 'Y' # check if input is yes
choice2 = save == 'N' # check if input is no

while not choice1 and not choice2: # check if valid input has been provided
    save = input('Please provide a correct input (Y or N)') # if invalid, request new input
    choice1 = save == 'Y' # re-run yes check
    choice2 = save == 'N' # re=run no check

if save == 'Y': #
    figure.savefig('NI_County_Map.png', dpi=300, bbox_inches='tight')

else:
    print('The process has now ended. To generate a new map, please re-run the script.')
