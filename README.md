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
## Infraestructura Utilizada
La infraestructura utilizada para la solución de los retos propuesto en el Codefest Ad Astra 2022 consistió de una solución Cloud a través de los servicios Azure para la ingesta de datos, procesamiento de datos y almacenamiento. Además, se utilizó una infraestructura local como interfaz gráfica para el despliegue del funcionamiento de cada una de las soluciones de los retos. A continuación se muestra una imagen que resumen la infraestructura utilizada.
## Estrategias Utilizadas
### **Análisis de Imágenes**
Para el análisis de imágenes se hizo uso de varias librerías de Python que nos facilitaban el uso y el procesamiento de las imágenes de diferentes formatos. Además se utilizo QGis como software para el visualización y localización de las imágenes y la potencia brindada por las herramientas cloud de Azure.
Las librerías que nos permitieron el uso y procesamiento de estas imágenes se describen a continuación:
* Osgeo
* Rasterio
* Numpy
* Pillow

### **Solución de retos**

Reto 1:  Alteración de Coordenadas

Para la solución del reto 1 se planteó un sistema de protección de la metadata en 2 etapas. 

La primera etapa de seguridad consistió en un cambio del sistema de referenciación de forma aleatoria, de esta forma, al tener un sistema de referenciación diferente genera una dificultad a la hora de poder entender la localización original de la imagen, ya que existen más de 10 mil tipos de sistemas de referenciación diferentes. 

La segunda etapa de seguridad y encriptación de la metadata consistió en generar una translación aleatoria de la transformación afín original, esto implica un cambio en la latitud y longitud de las coordenadas originales. 

La combinación de estas 2 etapas de seguridad generan que sea muy difícil recuperar la información de la metadata original.

Reto 2:  Previsualización de Imágenes

Para la solución del reto 2 se tomaron 2 acciones que permitían generar una compresión lossy con un gran ratio de compresión sin perder la esencia inicial de la imagen (perfecto para la previsualización de la imagen).

La primera acción que se tomó fue realizar una compresión LERT (algoritmo lossy con gran ratio de compresión pero velocidad baja) con 2 agentes, esto, en el promedio de las imágenes implicaba una reducción del 50%-60%.

Posteriormente, después de tener el output de la compresión LERT se realizó una reducción de la resolución lo suficientemente pequeña para alcanzar al menos el 5% del tamaño de la imagen original. Esta transformación se hizo tomando en cuenta la transformación de la metadata para que esta se mantuviera de manera integra así la calidad de la imagen fuera menor.

Reto 3: Cifrado y compresión

Para la solución del reto 3 se tomaron 3 acciones para lograr el objetivo deseado. 

La primera de estas acciones fue dividir la imagen en 9 fragmentos, esto con el fin de tomar fracciones de las imágenes que tuvieran una correlación de píxeles más alta que la correlación de la imagen completa. 

La segunda acción es tomar cada fragmento obtenido en el paso anterior y comprimirlas a través del algoritmo de compresión "Deflate" (lossless).

Por último, se realizó la unión de cada fragmento comprimido para obtener como resultado la imagen original pero comprimida sin perder calidad a un ratio de 1:10.
