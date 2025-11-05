from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class Personal:
    id: int
    nombre: str
    rol: str
    contacto: dict
    fecha_alta: datetime.date
    activo: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rol": self.rol,
            "contacto": self.contacto,
            "fecha_alta": self.fecha_alta.isoformat(),
            "activo": self.activo,
        }

    @classmethod
    def from_dict(cls, d):
        import datetime
        d2 = dict(d)
        d2["fecha_alta"] = datetime.date.fromisoformat(d2["fecha_alta"]) if isinstance(d2["fecha_alta"], str) else d2["fecha_alta"]
        return cls(**d2)
