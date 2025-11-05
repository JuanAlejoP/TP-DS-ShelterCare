"""
Archivo integrador generado automaticamente
Directorio: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades
Fecha: 2025-11-05 03:19:09
Total de archivos integrados: 7
"""

# ================================================================================
# ARCHIVO 1/7: animal.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/animal.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 2/7: gato.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/gato.py
# ================================================================================

from .animal import Animal

class Gato(Animal):
    especie = "Cat"

    def __init__(self, *args, **kwargs):
        super().__init__(especie=self.especie, *args, **kwargs)


# ================================================================================
# ARCHIVO 3/7: historia_medica.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/historia_medica.py
# ================================================================================

from dataclasses import dataclass, field
from typing import List
import datetime

@dataclass
class Examen:
    fecha: datetime.date
    veterinario_id: int
    hallazgos: str
    diagnostico: str
    prescripcion: List[dict] = field(default_factory=list)

@dataclass
class HistoriaMedica:
    animal_id: int
    examenes: List[Examen] = field(default_factory=list)

    def to_dict(self):
        return {"animal_id": self.animal_id, "examenes": [{"fecha": e.fecha.isoformat(), "veterinario_id": e.veterinario_id, "hallazgos": e.hallazgos, "diagnostico": e.diagnostico, "prescripcion": e.prescripcion} for e in self.examenes]}

    @classmethod
    def from_dict(cls, d):
        examenes = []
        import datetime
        for e in d.get("examenes", []):
            examenes.append(Examen(fecha=datetime.date.fromisoformat(e["fecha"]), veterinario_id=e["veterinario_id"], hallazgos=e["hallazgos"], diagnostico=e["diagnostico"], prescripcion=e.get("prescripcion", [])))
        return cls(animal_id=d["animal_id"], examenes=examenes)


# ================================================================================
# ARCHIVO 4/7: inventario.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/inventario.py
# ================================================================================

from dataclasses import dataclass

@dataclass
class ProductoInventario:
    sku: str
    nombre: str
    categoria: str
    cantidad: int
    unidad: str
    punto_reorden: int = 10

    def to_dict(self):
        return {"sku": self.sku, "nombre": self.nombre, "categoria": self.categoria, "cantidad": self.cantidad, "unidad": self.unidad, "punto_reorden": self.punto_reorden}

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


# ================================================================================
# ARCHIVO 5/7: perro.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/perro.py
# ================================================================================

from .animal import Animal

class Perro(Animal):
    especie = "Dog"

    def __init__(self, *args, **kwargs):
        super().__init__(especie=self.especie, *args, **kwargs)


# ================================================================================
# ARCHIVO 6/7: personal.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/personal.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 7/7: sede.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/entidades/sede.py
# ================================================================================

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


