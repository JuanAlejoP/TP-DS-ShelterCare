from src.entidades.sede import Sede, Zona
from typing import Optional

class SedeService:
    def __init__(self):
        self._sede: Optional[Sede] = None

    def crear_sede(self, nombre: str, direccion: str, capacidad_total: int, zonas: list):
        zonas_obj = [Zona(**z) for z in zonas]
        self._sede = Sede(nombre=nombre, direccion=direccion, capacidad_total=capacidad_total, zonas=zonas_obj)
        return self._sede

    def get_sede(self) -> Optional[Sede]:
        return self._sede

    def ocupar_zona(self, nombre_zona: str) -> None:
        if not self._sede:
            raise ValueError("No hay sede creada")
        for z in self._sede.zonas:
            if z.nombre == nombre_zona:
                if z.ocupacion >= z.capacidad:
                    raise ValueError("Capacidad insuficiente en zona")
                z.ocupacion += 1
                return
        raise ValueError("Zona no encontrada")
