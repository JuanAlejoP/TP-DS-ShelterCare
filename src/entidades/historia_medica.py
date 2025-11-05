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
