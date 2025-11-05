"""
Archivo integrador generado automaticamente
Directorio: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src
Fecha: 2025-11-05 03:19:09
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: constantes.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/constantes.py
# ================================================================================

from typing import List

# capacidades
CAPACIDAD_MINIMA = 1

# tiempos
TIEMPO_SEGUIMIENTO_POST_ADOPCION_DIAS: List[int] = [7, 30, 90]

# alimentacion
RACION_POR_KG_PERRO = 0.03  # 3% del peso corporal (ejemplo)
RACION_POR_KG_GATO = 0.025

# sensores
TEMP_MIN_OK = 15.0  # grados C
TEMP_MAX_OK = 28.0
HUMEDAD_MIN_OK = 30.0
HUMEDAD_MAX_OK = 70.0

# inventario
PUNTO_REORDEN_DEFAULT = 10


