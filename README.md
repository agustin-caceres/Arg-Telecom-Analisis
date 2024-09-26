# Proyecto de Análisis del Sector Telecomunicaciones

## Contexto

Este proyecto tiene como objetivo analizar el sector de las telecomunicaciones, abarcando los servicios de  **Internet** ,  **Telefonía Móvil** , y **Conectividad** en Argentina, utilizando diversas fuentes de datos provistas por organismos oficiales.

El análisis incluye el procesamiento de los datos, la creación de una base de datos SQL y la construcción de un dashboard interactivo que permitirá visualizar distintos KPIs y métricas relevantes.

### Objetivos Principales:

1. **Análisis Exploratorio de Datos (EDA)** : Detectar patrones, outliers y distribuciones.
2. **Desarrollo de un Dashboard** : Crear un tablero interactivo que muestre los KPIs más relevantes del sector.
3. **KPIs** : Definir, calcular y visualizar KPIs claves como el acceso a internet por provincia.
4. **Base de Datos SQL** : Crear una base de datos que estructure los datos procesados de manera eficiente y permita la integración de distintos datasets.

---

## Proceso ETL

Se realizó un proceso de **Extracción, Transformación y Carga (ETL)** para los datasets más relevantes al proyecto. El objetivo del ETL fue limpiar y estructurar los datos para su posterior análisis y uso en la base de datos.

### Datasets Utilizados:

1. **Internet** :

* Contiene información sobre accesos a internet, velocidades de conexión, ingresos, penetración en hogares y población.

1. **Telefonía Móvil** :

* Incluye información sobre llamadas, SMS, minutos consumidos, ingresos y penetración del servicio.

1. **Mapa de Conectividad** :

* Proporciona datos sobre la conectividad en diversas localidades, incluyendo tecnologías de acceso y cobertura de red.

### Proceso de ETL:

El proceso de ETL se aplicó a cada dataset por separado. A continuación se detallan las etapas del ETL para los datasets de Internet, Telefonía Móvil y Mapa de Conectividad:

1. **Internet** :

* Se procesaron y exportaron  **7 tablas** : `accesos_por_velocidad`, `accesos_tecnologia_localidad`, `accesos_velocidad_localidad`, `ingresos_servicios_internet`, `penetracion_internet_hogares`, `penetracion_internet_poblacion`, y `velocidad_media_provincia`.

1. **Telefonía Móvil** :

* Se procesaron y exportaron  **6 tablas** : `accesos_telefonia_movil`, `ingresos_telefonia_movil`, `llamadas_salientes`, `minutos_salientes`, `penetracion`, y `sms`.

1. **Mapa de Conectividad** :

* Se procesó una tabla llamada `mapa_conectividad`, que incluye información geográfica y de conectividad por localidad.

---

## Arquitectura de la Base de Datos

La base de datos creada en **PostgreSQL** será la fuente de este proyecto. Se decidió normalizar las tablas y mantener una estructura eficiente y clara para la integración de los datasets. A continuación se detallan las tablas principales y complementarias que formarán parte de la base de datos:

### Tablas Principales:

1. **Internet** :

* `accesos_por_velocidad_provincia`: Almacena los accesos a internet por velocidad de conexión y provincia.
* `accesos_tecnologia_localidad`: Almacena los tipos de acceso a internet por localidad (ADSL, cablemodem, fibra óptica, etc.).
* `accesos_por_velocidad_localidades`: Registra las velocidades de conexión disponibles por localidad.
* `ingresos_servicios_internet`: Detalla los ingresos obtenidos por los servicios de internet en miles de pesos.
* `penetracion_internet_hogares`: Almacena la penetración de internet por cada 100 hogares.
* `penetracion_internet_poblacion`: Almacena la penetración de internet por cada 100 habitantes.
* `velocidad_media_provincia`: Registra la velocidad media de bajada de internet por provincia.

2. **Telefonía Móvil** :

* `accesos_telefonia_movil`: Registra el acceso a la telefonía móvil por tecnología y localidad.
* `ingresos_telefonia_movil`: Detalla los ingresos por el servicio de telefonía móvil.
* `llamadas_salientes`: Almacena los datos sobre las llamadas salientes por periodo.
* `minutos_salientes`: Registra los minutos de llamadas salientes por provincia y periodo.
* `penetracion_telefonia_movil`: Registra la penetración de la telefonía móvil por provincia.
* `sms_salientes`: Almacena los SMS salientes por provincia y periodo.

3. **Mapa de Conectividad** :

* `mapa_conectividad`: Incluye información sobre la cobertura de diversas tecnologías de acceso (ADSL, fibra óptica, 4G, etc.) por localidad.

### Tablas de Apoyo:

1. **Provincias** :

* `provincias`: Incluye los nombres únicos de las provincias.

1. **Periodos** :

* `periodos`: Registra los distintos periodos de tiempo (Año y Trimestre).

1. **Localidades** :

* `localidades`: Almacena las localidades únicas, asociadas a sus provincias, con coordenadas de latitud y longitud.

---

## Normalización y Decisiones de Modelado

Durante la creación de la base de datos, se tomaron las siguientes decisiones clave:

1. **División de la tablas**:
   Se crearon tablas de apoyo (Provincias - Localidades - Periodos) respondiendo a la necesidad de evitar redundancia de columnas iguales en distintas tablas.
3. **Normalización de nombres de provincias** :
   Se estandarizó el nombre de las provincias, convirtiéndolas a todas en minúsculas.


---

### Cómo Ejecutar el Proyecto

1. **Requisitos Previos** :

* Librerías de Python: pandas, numpy, matplotlib, seaborn, psycopg2, etc.
* Motor de base de datos  **PostgreSQL** .

1. **Pasos para Reproducir el Proyecto** :

* Clonar el repositorio.
* Ejecutar los notebooks de ETL para obtener los datasets procesados.
* Cargar los datasets en la base de datos SQL.
* Ejecutar el análisis exploratorio de datos y generar las visualizaciones.
