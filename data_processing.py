import geopandas as gpd
import pandas as pd

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

# def road_handles