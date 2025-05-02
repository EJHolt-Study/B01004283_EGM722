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
    clipped_objects = gpd.clip(input,overlay,keep_geom_type=True) # Adding clipped input GDF objects to new list
    # keep_geom_type=True ensures input geometry type remains consistent
    # clipped_gpd = gpd.GeoDataFrame(pd.concat(clipped_objects, ignore_index=True)) # Creates combined GDF of clipped GDF objects

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

    if road_type == 'motorway':
        symbology = ShapelyFeature(layer['geometry'],proj_crs,color='tab:blue',linewidth=thickness,facecolor='none')

    elif road_type == 'dualcarr':
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:cyan', linewidth=thickness,facecolor='none')

    elif road_type == 'aclass':
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:orange', linewidth=thickness,facecolor='none')

    elif road_type == 'bclass':
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:olive', linewidth=thickness,facecolor='none')

    elif road_type == 'minor':
        symbology = ShapelyFeature(layer['geometry'], proj_crs, color='tab:gray', linewidth=thickness,facecolor='none')

    else:
        raise ValueError("Provided road class invalid")

    return symbology

def legend_items(labels, colors, edge='k', alpha=1):

    ################# DELETE LINE ONCE FUNCTION IS EDITED ##########################
    """
    Generate matplotlib patch handles to create a legend of each of the features in the map.

    Parameters
    ----------

    labels : list(str)
        the text labels of the features to add to the legend

    colors : list(matplotlib color)
        the colors used for each of the features included in the map.

    edge : matplotlib color (default: 'k')
        the color to use for the edge of the legend patches.

    alpha : float (default: 1.0)
        the alpha value to use for the legend patches.

    Returns
    -------

    handles : list(matplotlib.patches.Rectangle)
        the list of legend patches to pass to ax.legend()
    """
    lc = len(colors)  # get the length of the color list
    handles = [] # create an empty list
    for ii in range(len(labels)): # for each label and color pair that we're given, make an empty box to pass to our legend
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[ii % lc], edgecolor=edge, alpha=alpha))
    return handles