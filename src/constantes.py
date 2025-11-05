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
