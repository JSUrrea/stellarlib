# Documento de Diseño
Documento de diseño de equipo "Stellar Coders"
## Estructura del código
**stellar.asarray**
stellar.asarray(a:str, b:int, c:list) --> Img
Parameters:
* a (str): Number of bla bla bla
* b :
* c:
Output: 

## Tutorial de instalación

**Desde github**

1. Acceder a https://github.com/JSUrrea/stellarlib

2. Click en código
 
3. Copiar la url HTTPS del repositorio
 
4. Clonar el repositorio al mismo nivel de su archivo de desarrollo
 
5. Añadir import stellarlib al incio de su código 

## Infraestructura Utilizada
La infraestructura utilizada para la solución de los retos propuesto en el Codefest Ad Astra 2022 consistió de una solución Cloud a través de los servicios Azure para la ingesta de datos, procesamiento de datos y almacenamiento. Además, se utilizó una infraestructura local como interfaz gráfica para el despliegue del funcionamiento de cada una de las soluciones de los retos. A continuación se muestra una imagen que resumen la infraestructura utilizada.

![Arquitectura AD Astra!](/Resources/ArquitectruraADAstra.png "Arquitectura AD Astra")

## Estrategias Utilizadas
### **Análisis de Imágenes**
Para el análisis de imágenes se hizo uso de varias librerías de Python que nos facilitaban el uso y el procesamiento de las imágenes de diferentes formatos. Además se utilizo QGis como software para el visualización y localización de las imágenes y la potencia brindada por las herramientas cloud de Azure.
Las librerías que nos permitieron el uso y procesamiento de estas imágenes se describen a continuación:
* Osgeo
* Rasterio
* Numpy
* Pillow
## Estructura de directorios del contenedor

### **Carpeta principal: adastra**

- **OutImages**

La carpeta contiene las imagenes relacionadas a cada uno de los retos antes y después del procesamiento. 

La imagen antes del procesamiento con su nombre convencional (Ej:recorte_3_m120_l4_20181228_rgbnn)

La imagen con su debida transformación según el reto (Ej:Reto2_recorte_3_m120_l4_20181228_rgbnn)

- **Temp**

La carpeta fué usada para guardar archivos intermedios durante el procesamiento

- **type1**

Carpeta dónde se encuentran imágenes fuente

- **type2**

Carpeta dónde se encuentran imágenes fuente

## **Documentación de las clases y métodos disponibles**

### Clases y métodos
**stellar.compress**

*stellarlib.compress(tif_path: str, grid: tuple) --> None*

**Descripción:** Comprime una imagen en un archivo .stellar

**Parémetros:**

-  **tif_path (str):**  Path de la imagen que se quiere comprimir.
- **grid (tuple):** Tamaño de la grilla en la cuál se quiere dividir la imagen a comprimir.

------------

 **stellar.decompress**
 
*stellarlib.decompress(stellar_file: str) --> Tiff*

**Descripción:** Descomprime una imagen .stellar en una imagen Tiff

**Parémetros:**

-  **stellar_file (str):**  Path del archivo .stellar que se quiere descomprimir.

------------

**stellar.secure_transfer**

*stellarlib.secure_transfer(real_password: str) --> def*

**Descripción:** Devuelve una función que valida el acceso a las imágenes

**Parémetros:**

-  **real_password (str):**  Clave a usar para validar al usuario.

------------

**stellar.encrypt_image**

*stellarlib.encrypt_image(image: str, out_path: str) --> def*

**Descripción:** Realiza un cambio aleatorio en el sistema de georreferenciación junto a una translación aleatoria. 

**Parémetros:**

-  **image: (str):**  Path de la imagen que se quiere encriptar sus coordenadas. 

-  **out_path: (str):**  Path de la imagen de salida con las coordenadas encriptadas. 

------------

**stellar.save_image**

*stellarlib.save_image(path: str) --> def*

**Descripción:** Guarda la imagen en el servicio de Azure. 

**Parémetros:**

-  **path: (str):**  Path de la imagen que se quiere guardar en Azure. 

------------

**stellar.create_visual**

*stellarlib.create_visual(path: str) --> def*

**Descripción:** Guarda una visualización de bajo tamaño de la imagen. 

**Parémetros:**

-  **in_path: (str):**  Ruta a la imagen que se desea reducir en tamaño. 

-  **out_path: (str):**   Ruta donde se guardará la visualización resultante.


## **Solución de retos**

**Reto 1:  Alteración de Coordenadas**

Para la solución del reto 1 se planteó un sistema de protección de la metadata en 2 etapas. 

La primera etapa de seguridad consistió en un cambio del sistema de referenciación de forma aleatoria, de esta forma, al tener un sistema de referenciación diferente genera una dificultad a la hora de poder entender la localización original de la imagen, ya que existen más de 10 mil tipos de sistemas de referenciación diferentes. 

La segunda etapa de seguridad y encriptación de la metadata consistió en generar una translación aleatoria de la transformación afín original, esto implica un cambio en la latitud y longitud de las coordenadas originales. 

La combinación de estas 2 etapas de seguridad generan que sea muy difícil recuperar la información de la metadata original.

![Reto 1!](/Resources/reto1.jpeg "reto1")

------------

**Reto 2:  Previsualización de Imágenes**

Para la solución del reto 2 se tomaron 2 acciones que permitían generar una compresión lossy con un gran ratio de compresión sin perder la esencia inicial de la imagen (perfecto para la previsualización de la imagen).

La primera acción que se tomó fue realizar una compresión LERT (algoritmo lossy con gran ratio de compresión pero velocidad baja) con 2 agentes, esto, en el promedio de las imágenes implicaba una reducción del 50%-60%.

Posteriormente, después de tener el output de la compresión LERT se realizó una reducción de la resolución lo suficientemente pequeña para alcanzar al menos el 5% del tamaño de la imagen original. Esta transformación se hizo tomando en cuenta la transformación de la metadata para que esta se mantuviera de manera integra así la calidad de la imagen fuera menor.

![Reto 2!](/Resources/reto2.jpeg "reto2")

------------

**Reto 3: Cifrado y compresión**

Para la solución del reto 3 se tomaron 3 acciones para lograr el objetivo deseado. 

La primera de estas acciones fue dividir la imagen en 9 fragmentos, esto con el fin de tomar fracciones de las imágenes que tuvieran una correlación de píxeles más alta que la correlación de la imagen completa. 

La segunda acción es tomar cada fragmento obtenido en el paso anterior y comprimirlas a través del algoritmo de compresión "Deflate" (lossless).

Por último, se realizó la unión de cada fragmento comprimido para obtener como resultado la imagen original pero comprimida sin perder calidad a un ratio de 1:10.

![Reto 3!](/Resources/reto3.jpeg "reto3")
