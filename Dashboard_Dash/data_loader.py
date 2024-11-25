import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Cargar credenciales del archivo .env
load_dotenv("C:/DYNAMO/ProyectoN2/credenciales.env")

def connect_db():
    """ Funcion para conectarse a la base de datos """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn




# -- FUNCIONES PARA EL KPI 1 --

def load_internet_penetration_data():
    """ Funcion para cargar los datos de penetracion de internet en hogares para el KPI 1 """
    conn = connect_db()
    
    # Consulta SQL
    query = """
    SELECT 
        p.nombre_provincia, 
        pe.anio, 
        pe.trimestre,
        ph.accesos_por_100_hogares
    FROM 
        penetracion_internet_hogares ph
    JOIN 
        provincias p ON ph.id_provincia = p.id_provincia
    JOIN 
        periodos pe ON ph.id_periodo = pe.id_periodo;
    """
    
    # Ejecutar consulta y cargar en DataFrame
    df = pd.read_sql(query, conn)
    
    # Cerrar conexión
    conn.close()
    
    return df


def cargar_datos_penetracion_mapa():
    """
    Carga los datos de penetración promedio por provincia desde la base de datos.

    Retorno:
    - DataFrame con las columnas 'nombre_provincia' y 'promedio_accesos'.
    """
    conn = connect_db()

    # Consulta SQL
    query = """
    SELECT 
        p.nombre_provincia, 
        AVG(ph.accesos_por_100_hogares) AS promedio_accesos
    FROM 
        penetracion_internet_hogares ph
    JOIN 
        provincias p ON ph.id_provincia = p.id_provincia
    JOIN 
        periodos pe ON ph.id_periodo = pe.id_periodo
    WHERE 
        pe.anio >= 2024
    GROUP BY 
        p.nombre_provincia;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Normalizar nombres de provincias para facilitar la coincidencia con GeoJSON
    df['nombre_provincia'] = df['nombre_provincia'].str.lower()
    return df




# -- FUNCIONES PARA EL KPI 2 --

def cargar_datos_cobertura_fibra():
    """
    Carga los datos de cobertura de fibra óptica y conectividad inalámbrica por localidad y provincia.

    Retorno:
    - DataFrame con las columnas 'localidad', 'nombre_provincia', 'fibra_optica', 'wireless' y 'poblacion'.
    """
    conn = connect_db()

    # Consulta SQL
    query = """
    SELECT 
        l.localidad, 
        p.nombre_provincia, 
        mc.fibra_optica, 
        mc.wireless, 
        mc.poblacion 
    FROM 
        mapa_conectividad mc
    JOIN 
        localidades l ON mc.id_localidad = l.id_localidad
    JOIN 
        provincias p ON l.id_provincia = p.id_provincia
    WHERE 
        mc.fibra_optica = TRUE OR mc.wireless = TRUE
    ORDER BY 
        p.nombre_provincia, l.localidad;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df




# -- FUNCIONES PARA EL KPI 3 --

def cargar_datos_accesos_movil():
    """
    Carga los datos de accesos a planes de telefonía móvil pospago y prepago por año y trimestre.

    Retorno:
    - DataFrame con las columnas 'anio', 'trimestre', 'total_accesos_pospago', y 'total_accesos_prepago'.
    """
    conn = connect_db()

    # Consulta SQL
    query = """
        SELECT 
            pe.anio,
            pe.trimestre,
            atm.total_accesos_pospago,
            atm.total_accesos_prepago
        FROM 
            accesos_telefonia_movil atm
        JOIN
            periodos pe ON atm.id_periodo = pe.id_periodo
        ORDER BY 
            pe.anio, pe.trimestre;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Función para generar el DataFrame
def get_provinces_data():
    df = {
        "Province Code": ["AR-C", "AR-B", "AR-K", "AR-H", "AR-U", "AR-X", "AR-W", "AR-E", "AR-P", "AR-Y", 
                          "AR-L", "AR-F", "AR-M", "AR-N", "AR-Q", "AR-R", "AR-A", "AR-J", "AR-D", "AR-Z", 
                          "AR-S", "AR-G", "AR-V", "AR-T"],
        "Province Name": ["CABA", "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", 
                          "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", 
                          "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
                          "Santiago del Estero", "Tierra del Fuego", "Tucumán"],
        "Value": [10, 20, 15, 30, 25, 40, 35, 50, 5, 45, 15, 20, 60, 55, 70, 65, 80, 75, 90, 85, 100, 95, 110, 105],
        "Latitude": [-34.6037, -36.6769, -28.4696, -27.4519, -43.7924, -31.4173, -27.4692, -32.0586, -26.1775, -24.1858, 
                     -36.6167, -29.4146, -32.8908, -27.3769, -38.9516, -40.8116, -24.7821, -30.8654, -33.3012, -49.3167, 
                     -31.6333, -27.7834, -54.8019, -26.8241],
        "Longitude": [-58.3816, -60.5588, -65.7852, -58.9867, -67.8076, -64.183, -58.8341, -60.4803, -58.1781, -65.3002, 
                      -64.2833, -66.8556, -68.8458, -55.8961, -68.0591, -63.0000, -65.4232, -68.8896, -66.3378, -67.7333, 
                      -60.7, -63.2513, -68.3030, -65.2226]
    }
    return pd.DataFrame(df)