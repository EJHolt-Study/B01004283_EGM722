import geopandas as gpd
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

def clip_features(input,overlay):
    """
    Clips a GeoDataFrame(GDF) to the geometric extent of another specified GDF.
    
    Parameters
    ----------
    input: GDF
        Layer that will be clipped. Can have point, line, or polygon geometry
    
    overlay: GDF
        Layer used to define extent of clipping. Requires polygon geometry

    Returns
    -------
    clipped_gdf: new clipped gdf, with input values clipped to geometry extent of overlay
    """
    clipped_objects = [] # Creates list to contain clipped objects of input layer
    clipped_objects = gpd.clip(input,overlay) # Adding clipped input GDF objects to new list
    # clipped_gpd = gpd.GeoDataFrame(pd.concat(clipped_objects, ignore_index=True)) # Creates combined GDF of clipped GDF objects

    return clipped_objects

def roads_symbology(layer,road_type):
    """
    Takes the subset of the road GDF and creates appropriate symbology for the road class.
    
    Parameters
    ----------
    layer: GDF
        Roads GDF for which the symbology with be created
    
    road_type: string
        Layer used to define extent of clipping. Requires polygon geometry

        Valid inputs - motorway, dualcarr, aclass, bclass, minor

    Returns
    -------
    road_symbology: class 'cartopy.feature.ShapelyFeature'

    """
    proj_crs = ccrs.UTM(29)  # create copy of project crs (EPSG: 2158 - UTM zone 29)

    if road_type == 'motorway':
        road_symbology = ShapelyFeature(layer['geometry'],proj_crs,color='blue',linewidth=2)

    elif road_type == 'dualcarr':
        road_symbology = ShapelyFeature(layer['geometry'], proj_crs, color='cyan', linewidth=1.5)

    elif road_type == 'aclass':
        road_symbology = ShapelyFeature(layer['geometry'], proj_crs, color='orange', linewidth=1)

    elif road_type == 'bclass':
        road_symbology = ShapelyFeature(layer['geometry'], proj_crs, color='olive', linewidth=0.75)

    elif road_type == 'minor':
        road_symbology = ShapelyFeature(layer['geometry'], proj_crs, color='blue', linewidth=2)

    return road_symbology

