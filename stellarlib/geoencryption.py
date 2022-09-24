import numpy as np
import rasterio


def secure_transfer(real_password):
    """
    Devuelve una función que valida el acceso a las imágenes
    real_password: Clave a usar para validar al usuario
    """

    def validate(in_path, out_path, user_password):
        """
        Devuelve información errada en caso de que la clave no sea válida
        in_path: Ruta de la imagen solicitada
        out_path: Ruta donde guardar la imagen
        user_password: Clave escrita por el usuario
        """

        # Leer la imagen
        file = rasterio.open(in_path)

        # Clave correcta
        if real_password == user_password:
            with rasterio.open(out_path, "w") as out:
                out.write(file)
            
        else:
            # Encriptar los metadatos
            encrypt_image(file, out_path)

    return validate


def encrypt_image(image, out_path):
    """
    image: Imagen a encriptar
    out_path: Ruta donde guardar la imagen cifrada
    """

    # Leer las bandas de la imagen
    band_array=[]
    for i in range(1,image.count+1):
        band_array.append(image.read(i))
    dataraster = np.stack(band_array)

    # Escribir la imagen alterando los metadatos
    with rasterio.open(
        out_path,
        'w', 
        driver = image.driver, 
        height = dataraster.shape[1], 
        width = dataraster.shape[2],
        count = dataraster.shape[0], 
        dtype = dataraster.dtype, 
        crs = 'EPSG:4326', 
        transform = [5.0,0,357200.13,0,-5,949926.02]
    ) as image_transformed:
        image_transformed.write(dataraster)

    return image_transformed

