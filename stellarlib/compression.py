import  os
from osgeo import gdal
import numpy as np
import rasterio
import rasterio.features
import rasterio.warp
import os
import numpy as np
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
import pickle
from PIL import Image

def compress(tif_path, grid=(10,10)):
    """
    Comprime la imagen completa dividiendo en regiones y comprimiendo cada una
    grid: Define en cuántas particiones dividir la imagen
    """
    # Opciones
    topts = gdal.TranslateOptions(creationOptions =['TFW=NO', 'COMPRESS=DEFLATE', 'PREDICTOR=2.0'])

    # Leer tiff
    meta = rasterio.open(tif_path).meta
    img = gdal.Open(tif_path)

    # De la imagen
    width = meta['width']
    height = meta['height']

    # De cada región
    w = [int(width/grid[0])] * grid[0]
    for i in range(width % grid[0]):
        w[i] += 1
    h = [int(height/grid[1])] * grid[1]
    for j in range(height % grid[1]):
        h[j] += 1

    # Verificar que la imagen se cubre completa
    assert sum(w) == width
    assert sum(h) == height

    # Puntos iniciales (left-top)
    x = 0
    y = 0

    # Temp placeholder
    TEMP = "temp_.tif"

    # Carpeta de resultado
    out_folder = tif_path.replace('.tif', '_compressed')
    os.makedirs(out_folder, exist_ok=True)

    # Save metadata
    base_name = tif_path.replace('.tif', '')
    pickle.dump(meta, open(os.path.join(out_folder, f"{base_name}_{grid[0]}x{grid[1]}.metadata"), "bw"))
    
    for i in range(grid[0]):
        
        for j in range(grid[1]):
            
            # Cortar
            gdal.Translate(TEMP, img, srcWin  = [x, y, w[i], h[j]])
            
            # Comprimir
            crop_name = tif_path.replace('.tif', f'_{i+1}x{j+1}.tif')
            name_compr = os.path.join(out_folder, crop_name)
            gdal.Translate(name_compr, TEMP, options=topts)
            
            y += h[j]
            
        x += w[i]
        
    # Create final compression file
    with ZipFile(out_folder + ".stellar", "w", ZIP_DEFLATED) as zf:
        for file in os.listdir(out_folder):
            zf.write(os.path.join(out_folder, file), arcname=file)
        
    # Clean up space
    shutil.rmtree(out_folder)
    os.remove(TEMP)
    

def decompress(stellar_file):
    with ZipFile(stellar_file, "r") as zf:
        
        for file_name in zf.namelist():
            if file_name.endswith(".metadata"):
                meta = file_name
                break
        base_name = meta[:meta.rindex("_")]
        grid = tuple(map(int, meta[meta.rindex("_")+1:].replace(".metadata", "").split("x")))
        
        with zf.open(meta) as file:
            meta = pickle.load(file)
        height = meta["height"]
        width = meta["width"]
        image = np.zeros((height, width))
        ########
        valid = np.zeros((height, width)).astype(bool)
        
        x = 0
        
        for i in range(grid[0]):
            
            y = 0
        
            for j in range(grid[1]):

                file_name = f'{base_name}_{i+1}x{j+1}.tif'
                
                with zf.open(file_name) as file:
                    
                    crop = np.array(Image.open(file))
                    h,w,_ = crop.shape
                    
                    image[y:y+h, x:x+w] = crop
                    #######
                    valid[y:y+h, x:x+w] = True
                    
                    y += h
                    
            x += w
            
        ########    
        assert valid.all()
        return image
    
recontruccion = decompress("recorte_mision79_linea2__compressed.stellar")