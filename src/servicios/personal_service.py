from typing import Dict
from src.entidades.personal import Personal
import datetime

class PersonalService:
    def __init__(self):
        self._personas: Dict[int, Personal] = {}
        self._next = 1
        self.persistencia = None

        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('personal') or []
        import datetime
        for d in data:
            p = Personal.from_dict(d)
            self._personas[p.id] = p
            self._next = max(self._next, p.id+1)

    def _save(self):
        if not self.persistencia:
            return
        data = [p.to_dict() for p in self._personas.values()]
        self.persistencia.save('personal', data)

    def crear_personal(self, nombre: str, rol: str, contacto: dict, fecha_alta=None) -> Personal:
        fecha_alta = fecha_alta or datetime.date.today()
        p = Personal(id=self._next, nombre=nombre, rol=rol, contacto=contacto, fecha_alta=fecha_alta)
        self._personas[self._next] = p
        self._next += 1
        self._save()
        return p

    def get(self, pid: int) -> Personal:
        return self._personas.get(pid)

    def list_all(self):
        return list(self._personas.values())
