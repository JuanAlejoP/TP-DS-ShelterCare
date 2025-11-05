from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Zona:
    nombre: str
    capacidad: int
    ocupacion: int = 0

    def to_dict(self):
        return {"nombre": self.nombre, "capacidad": self.capacidad, "ocupacion": self.ocupacion}

@dataclass
class Sede:
    nombre: str
    direccion: str
    capacidad_total: int
    zonas: List[Zona] = field(default_factory=list)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "direccion": self.direccion,
            "capacidad_total": self.capacidad_total,
            "zonas": [z.to_dict() for z in self.zonas]
        }

    @classmethod
    def from_dict(cls, d):
        zonas = [Zona(**z) for z in d.get("zonas", [])]
        return cls(nombre=d["nombre"], direccion=d["direccion"], capacidad_total=d["capacidad_total"], zonas=zonas)
