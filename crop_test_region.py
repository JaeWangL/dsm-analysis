from fiona.crs import from_epsg
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import os
    
def get_gdf_features(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def crop_raster_by_coordinates(input_path: str, min_x: float, min_y: float, max_x: float, max_y: float) -> str:
    input_dir = os.path.dirname(input_path)
    input_filename_without_ext = os.path.splitext(os.path.basename(input_path))[0]
    input_extensions = os.path.splitext(os.path.basename(input_path))[1]
    out_path = '{0}/{1}{2}'.format(input_dir, 'cropped_' + input_filename_without_ext, input_extensions)
    
    data = rasterio.open(input_path)
    bbox = box(min_x, min_y, max_x, max_y)
    epsg_code = int(data.crs.data['init'][5:])
    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(epsg_code)) 
    geo = geo.to_crs(crs=data.crs.data)
    
    coords = get_gdf_features(geo)
    out_img, out_transform = mask(data, shapes=coords, crop=True)
    out_meta = data.meta.copy()
    out_meta.update({"driver": "GTiff",
        "height": out_img.shape[1],
        "width": out_img.shape[2],
        "transform": out_transform,
        "crs": data.crs
    })
    
    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(out_img)
        
    return out_path

