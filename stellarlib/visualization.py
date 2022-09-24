from osgeo import gdal
import rasterio


def create_visual(in_path, out_path):
    """
    Guarda una visualización de bajo tamaño de la imagen 
    in_path: Ruta a la imagen que se desea reducir en tamaño
    out_path: Ruta donde se guardará la visualización resultante
    """
    
    # Leer datos
    dataset = gdal.Open(in_path)
    prope = rasterio.open(in_path)

    # Resize
    gdal.Warp(out_path, dataset, xRes = 5, yRes = 5, format = prope.driver)

