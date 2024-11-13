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
