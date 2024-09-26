-- Obtener la cantidad de accesos a internet por provincia y año:

SELECT p.nombre_provincia, pe.anio, SUM(avp.total_accesos) AS total_accesos
FROM accesos_velocidad_provincia avp
JOIN provincias p 
	ON avp.id_provincia = p.id_provincia
JOIN periodos pe 
	ON avp.id_periodo = pe.id_periodo
GROUP BY 
	p.nombre_provincia, pe.anio
ORDER BY 
	pe.anio, total_accesos DESC;

-- Consulta de ingresos totales por servicio de internet por año

SELECT pe.anio, SUM(isi.ingresos_miles_pesos) AS total_ingresos
FROM ingresos_servicios_internet isi
JOIN periodos pe 
	ON isi.id_periodo = pe.id_periodo
GROUP BY pe.anio
ORDER BY pe.anio;

-- Penetración de internet en los hogares por provincia y año

SELECT p.nombre_provincia, pe.anio, ph.accesos_por_100_hogares
FROM penetracion_internet_hogares ph
JOIN provincias p 
	ON ph.id_provincia = p.id_provincia
JOIN periodos pe 
	ON ph.id_periodo = pe.id_periodo
ORDER BY pe.anio, ph.accesos_por_100_hogares DESC;

-- Velocidad media de conexión a internet por provincia

SELECT p.nombre_provincia, vmp.mbps_media_bajada
FROM velocidad_media_provincia vmp
JOIN provincias p 
	ON vmp.id_provincia = p.id_provincia
ORDER BY vmp.mbps_media_bajada DESC;



