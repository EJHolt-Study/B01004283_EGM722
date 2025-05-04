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
    clipped_objects = gpd.clip(input,overlay, # Adding clipped input GDF into new GDF objects to new list
                        keep_geom_type=True) # keep_geom_type=True ensures input geometry type remains consistent

    return clipped_objects

def roads_symbology(layer, road_type,thickness, kwargs=None):
    """
    Takes the subset of the road GDF and creates appropriate symbology for the road class.
    
    Parameters
    ----------
    layer: GDF
        Roads GDF for which the symbology with be created
    
    road_type: string
        Layer used to define extent of clipping. Requires polygon geometry

        Valid inputs - motorway, dualcarr, aclass, bclass, minor

    thickness: float
        Thickness of line layer symbology

    Returns
    -------
    road_symbology: class 'cartopy.feature.ShapelyFeature'

    """
    proj_crs = ccrs.UTM(29)  # create copy of project crs (EPSG: 2158 - UTM zone 29)

    symbology = layer

    if road_type == 'motorway': # set symbology for motorway GDF
        symbology = ShapelyFeature(layer['geometry'],proj_crs,color='tab:blue',linewidth=thickness,facecolor='none')

    elif road_type == 'dualcarr': # set symbology for dual-carriageway GDF
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:cyan', linewidth=thickness,facecolor='none')

    elif road_type == 'aclass': # set symbology for a-roads GDF
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:orange', linewidth=thickness,facecolor='none')

    elif road_type == 'bclass': # set symbology for b-roads GDF
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:olive', linewidth=thickness,facecolor='none')

    elif road_type == 'minor': # set symbology for minor roads GDF
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:gray', linewidth=thickness,facecolor='none')

    else: # return error message if invaild road type is provided
        raise ValueError("Provided road class invalid")

    return symbology
