# Relevamiento de Precios de Planes de Celular

## 📋 Acerca del Proyecto

Este proyecto tiene como objetivo principal el relevamiento de precios y características de los planes de celular ofrecidos por las empresas **Claro**, **Movistar** y **Personal**.  
El modelo desarrollado permite extraer información actualizada directamente desde las páginas web oficiales de cada operadora a partir de un archivo `.xlsx` que contiene las URLs de los planes. Entre la información extraída se incluyen: 

- Nombre del plan y nombre completo.
- Precio.
- Cantidad de gigas disponibles.

## 📦 Instalación

1. **Clona este repositorio:**
2. **Navega al directorio del proyecto:**
3. **Instala las dependencias:**

## 🖥️ Uso

Ejecuta el script mediante el siguiente comando:
python celular.py

## 🛠️ Ejecución del Script

El código está diseñado para realizar los siguientes pasos:

1. **Importar librerías necesarias:** Configura el entorno de trabajo cargando las dependencias requeridas.
2. **Cargar el archivo `.xlsx`:** Contiene todas las URLs a procesar, permitiendo filtrar por empresa (Claro, Movistar o Personal).
3. **Verificación de URLs:** Utiliza la librería `requests` para validar el acceso a cada enlace.
4. **Extracción de datos por empresa:** 
   - Obtiene las URLs de cada plan.
   - Extrae información clave como el nombre y el precio de los planes.
5. **Consolidación de datos:** Los precios por empresa se almacenan en dataframes separados que luego se concatenan en un único dataframe con la información consolidada. Este se exporta a un archivo `.xlsx`.
6. **Descarga de PDFs:** Por cada URL se descargan los PDFs asociados a las páginas de los planes analizados.

## ⚠️ Advertencia

Este código es **inestable**, ya que las páginas web de las operadoras pueden cambiar su estructura sin previo aviso. Si esto ocurre, será necesario ajustar el código para adaptarse a los nuevos parámetros y estructuras de cada sitio.
