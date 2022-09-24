import os
from azure.storage.blob import BlobServiceClient, BlobClient


def save_image(path):
    """
    Guarda la imagen en el servicio de Azure
    """
    # Conectarse
    connection_string = "DefaultEndpointsProtocol=https;AccountName=codefeststellarcoders;AccountKey=IIRtc+nuKUOT7dQU+CFt9Vgt3JTNTB6DO6r/wJ8Dq96PNS4nfOUQy0pzKF8FGXEGcbqhkJLP66G7+AStK2cHQw=="
    BlobServiceClient.from_connection_string(conn_str=connection_string)
    blob = BlobClient.from_connection_string(
        conn_str = connection_string, 
        container_name = "adastra", 
        blob_name = os.path.split(path)[1]
    )

    # Escribir
    with open(path, "rb") as data:
        blob.upload_blob(data)