# Import support packages
import os
import numpy as np
import rasterio as rio
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib_map_utils.core.north_arrow import NorthArrow, north_arrow
from matplotlib_map_utils.core.scale_bar import ScaleBar, scale_bar
#from pygments.styles.dracula import foreground
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from shapely import box
from cartopy.feature import ShapelyFeature
from data_processing import clip_features
from data_processing import roads_symbology

## Setup project datasets ##
#-----------------------------------------------------------------------------------------------------------------------
# Importing vector datasets as GeoDataFrames (GDF)
outline = gpd.read_file(os.path.abspath('data_files/NI_outline.shp')) # load NI Border Outline - Shapefile(Polygon)
lakes = gpd.read_file(os.path.abspath('data_files/Lake_Water_Bodies_2016.shp')) # load NI lake bodies - Shapefile(polygon)
settlements = gpd.read_file(os.path.abspath('data_files/settlements-2015-above-500-threshold.shp')) # load NI Settlements (pop. over 500) - Shapefile(Polygon)
counties = gpd.read_file(os.path.abspath('data_files/Counties.shp')) # load NI County Boundaries - Shapefile(Polygon)
roads = gpd.read_file(os.path.abspath('data_files/NI_roads.shp')) # load NI Road Network - Shapefile(Line)


# Converting GDFs to project CRS (EPSG: 2158)
outline = outline.to_crs(epsg=2158)
lakes = lakes.to_crs(epsg=2158)
settlements = settlements.to_crs(epsg=2158)
counties = counties.to_crs(epsg=2158)
roads = roads.to_crs(epsg=2158)

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

# Clipping map features based on specified map based on selection
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
    map_roads = roads # updating variable name to match remaining script
    map_settlements = settlements # updating variable name to match remaining script

## Generating map layers ##
#-----------------------------------------------------------------------------------------------------------------------
# Create figure and map axis
proj_crs = ccrs.UTM(29) # create copy of project crs (EPSG: 2158 - UTM zone 29)
figure = plt.figure(figsize=(10,10)) # creating 10" by 10" figure
axes = plt.axes(projection=proj_crs) # create the map axes on the figure with project crs

# Set map extent
minx,miny,maxx,maxy = map_counties.total_bounds # create map extent variables using selected area
axes.set_extent([minx,maxx,miny,maxy],crs=proj_crs) # setting axes extent to variables, using project crs

# Add base color to represent lake bodies and coastal regions
base = gpd.GeoDataFrame(geometry=[box(minx,miny,maxx,maxy)],crs=proj_crs) # create box GDF covering plot bounds
base_colour = ShapelyFeature(base['geometry'],
                             proj_crs,edgecolor='none',facecolor='lightblue') # define symbology for base layer
axes.add_feature(base_colour,zorder=0) # add base layer to map, zorder used ensure plotting as bottom layer

# Add NI outline to provide land background
land_base = ShapelyFeature(outline['geometry'],proj_crs,edgecolor='none',
                           facecolor='green') # define symbology for land background layer
axes.add_feature(land_base,zorder=1) # add land background to map above base layer

# Add NI lake bodies shapefile
map_lakes = ShapelyFeature(lakes['geometry'],proj_crs,edgecolor='none',
                           facecolor='blue') # define lakes symbology
axes.add_feature(map_lakes,zorder=2) # add lakes polygons to map above base layer and land background

# Adding map features
map_counties = ShapelyFeature(counties['geometry'],proj_crs,edgecolor='k',facecolor='none') # defining county details...
#... with black outline and transparent fill
axes.add_feature(map_counties) # Add county layer to map axes

# Separating road GDF into the primary road types
roads_motorways = map_roads[map_roads['Road_class']=='MOTORWAY'] # extracting all motorway road sections
roads_dualcarr = map_roads[map_roads['Road_class']=='DUAL_CARR'] # extracting all dual-carriageway road sections
roads_aclass = map_roads[map_roads['Road_class']=='A_CLASS'] # extracting all A-road sections
roads_bclass = map_roads[map_roads['Road_class']=='B_CLASS'] # extracting all B-road sections
# Grouping remaining minor road types
roads_minor = map_roads[map_roads['Road_class'].isin
                            (['<4M_TARRED','<4M_T_OVER','CL_MINOR','CL_M_OVER'])] # extracting all minor road sections

# Specifying map layers based on user selection
if select_edited in counties['CountyName'].unique(): # check if selection is a specific county

    # Add map title
    title = str(f'County {select_edited} Road Network and Urban Areas') # Create string for title w/ specific county
    plt.title(title, # Add title w/ selected county
               loc='center') # align title to centre of the axes

    # Generate road features and symbology for map plot, using roads_symbology function
    roads_motorways = roads_symbology(roads_motorways, 'motorway', 2)  # apply motorway symbology
    roads_dualcarr = roads_symbology(roads_dualcarr, 'dualcarr', 1)  # apply dual-carriageway symbology
    roads_aclass = roads_symbology(roads_aclass, 'aclass', 0.75)  # apply A-road symbology
    roads_bclass = roads_symbology(roads_bclass, 'bclass', 0.6)  # apply B-road symbology
    roads_minor = roads_symbology(roads_minor, 'minor', 0.5)  # apply minor road symbology

    # Add all road types to the plot
    axes.add_feature(roads_motorways)  # add motorways to map
    axes.add_feature(roads_dualcarr)  # add dual-carriageways to map
    axes.add_feature(roads_aclass)  # add A-roads to map
    axes.add_feature(roads_bclass)  # add B-roads to map
    axes.add_feature(roads_minor)  # add minor roads to map

    # Selecting appropriate urban areas for map scale
    map_settlements = map_settlements[map_settlements['Band'].isin # create updated version of GDF
                    (['A','B','C','D','E','F'])] # keep all urban areas with population>2,500

elif select_edited == 'All': # check if all counties have been selected

    # Add map title
    plt.title('Northern Ireland Primary Road Network and Urban Areas',  # Add title w/ selected county
               loc='center')  # align title to centre of the axes

    # Generate road features and symbology for map plot, using roads_symbology function
    # Add increased linewidth to account for smaller map scale
    roads_motorways = roads_symbology(roads_motorways, 'motorway', 2)  # apply motorway symbology
    roads_dualcarr = roads_symbology(roads_dualcarr, 'dualcarr', 1.5)  # apply dual-carriageway symbology
    roads_aclass = roads_symbology(roads_aclass, 'aclass', 1)  # apply A-road symbology
    roads_bclass = roads_symbology(roads_bclass, 'bclass', 0.75)  # apply B-road symbology

    # Add all road features except minor roads
    axes.add_feature(roads_motorways) # add motorways to map
    axes.add_feature(roads_dualcarr) # add dual-carriageways to map
    axes.add_feature(roads_aclass) # add A-roads to map
    axes.add_feature(roads_bclass) # add B-roads to map

    # Selecting appropriate urban areas for map scale
    map_settlements = map_settlements[map_settlements['Band'].isin
                    (['A', 'B', 'C','D'])]  # keep all urban areas with population>10,000

# Generate symbology for settlements layer
# Creating cartopy feature class for urban settlements layer, with translucent fill and dashed outline
settlements_symbology = ShapelyFeature(map_settlements['geometry'],proj_crs,
                                       edgecolor='dimgray',facecolor='gray',linewidth=1,alpha=0.7)

axes.add_feature(settlements_symbology) # Add settlement polygons to map

# Add map labels for urban areas (settlements)
settlement_labels = map_settlements # creating new GDF to for label generation
settlement_labels['geometry'] = settlement_labels['geometry'].centroid # Converts GDF geometry to centroid point
for ind, row in settlement_labels.iterrows(): # iterate across the rows in the GDF
    xval, yval = row.geometry.x, row.geometry.y # obtain x and y co-ordinate values for each row
    axes.text( # add settlement label to map figure
            xval,yval, # specify label location
            row['Name'].title(), # add label name in title case
            color='black',
            path_effects=[pe.withStroke(linewidth=2,foreground='white')],# Add white border to labels
            fontsize=7, # select font size
            transform=proj_crs) # confirm crs as EPSG:2158

## Generating additional map features
#-----------------------------------------------------------------------------------------------------------------------
# Add North Arrow
northarrow = NorthArrow( # create North Arrow class
    location="upper left", # position in upper left of axis
    scale=0.3, # set size as 0.5"
    rotation={"degrees":0})  # set rotation as 0
axes.add_artist(northarrow) # add North Arrow to map

# Add Scale Bar
sbar = ScaleBar( # create Scale Bar class
                location='lower left', # position in bottom left of axis
                style="ticks",bar={"projection":2158,"minor_type":"first"}, # define line style and division locations
                labels={"style":"major"}) # add labels to all major divisions
axes.add_artist(sbar) # add Scale Bar to map

# Add map legend

# Plotting the map
#-----------------------------------------------------------------------------------------------------------------------
print('Once you have reviewed the map, please close the figure window')
plt.show() # show map figure in pop-out window

# Saving map plot
#-----------------------------------------------------------------------------------------------------------------------
save = input('Would you like to save the map (Y/N): ') # new user input parameter to select if map should be saved
choice1 = save == 'Y' # check if input is yes
choice2 = save == 'N' # check if input is no

while not choice1 and not choice2: # check if valid input has been provided
    save = input('Please provide a correct input (Y or N)') # if invalid, request new input
    choice1 = save == 'Y' # re-run yes check
    choice2 = save == 'N' # re=run no check

if save == 'Y': # if user selects yes, save map as png
    figure.savefig('NI_County_Map.png', dpi=300, bbox_inches='tight')
    # after saving, print end message
    print('The process has now ended. To generate a new map, please re-run the script.')

else: # if user selects no, print end message
    print('The process has now ended. To generate a new map, please re-run the script.')
