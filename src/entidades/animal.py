from dataclasses import dataclass, field
from typing import Optional
import datetime

@dataclass
class Animal:
    id: int
    especie: str
    nombre: Optional[str]
    edad_meses: int
    sexo: str
    fecha_ingreso: datetime.date
    estado: str = "activo"
    zona: Optional[str] = None
    peso_kg: float = 0.0

    def to_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "nombre": self.nombre,
            "edad_meses": self.edad_meses,
            "sexo": self.sexo,
            "fecha_ingreso": self.fecha_ingreso.isoformat(),
            "estado": self.estado,
            "zona": self.zona,
            "peso_kg": self.peso_kg,
        }

    @classmethod
    def from_dict(cls, d):
        d2 = dict(d)
        d2["fecha_ingreso"] = datetime.date.fromisoformat(d2["fecha_ingreso"]) if isinstance(d2["fecha_ingreso"], str) else d2["fecha_ingreso"]
        return cls(**d2)
