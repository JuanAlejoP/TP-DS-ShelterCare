from typing import Dict
from src.entidades.animal import Animal
from src.patrones.factory.animal_factory import AnimalFactory
import datetime

class AnimalService:
    def __init__(self, persistencia=None):
        self._animales: Dict[int, Animal] = {}
        self._next = 1
        self.persistencia = persistencia
        self._quarantine_service = None

    def ingresar_animal(self, especie: str, nombre: str = None, edad_meses: int = 0, sexo: str = 'U', zona: str = None, peso_kg: float = 0.0):
        a = AnimalFactory.crear_animal(especie, id=self._next, nombre=nombre, edad_meses=edad_meses, sexo=sexo, fecha_ingreso=datetime.date.today(), zona=zona, peso_kg=peso_kg)
        self._animales[self._next] = a
        self._next += 1
        return a

    def get(self, aid: int) -> Animal:
        return self._animales.get(aid)

    def list_all(self):
        return list(self._animales.values())

    def persist_all(self):
        if not self.persistencia:
            return
        data = [a.to_dict() for a in self._animales.values()]
        self.persistencia.save('animales', data)

    def load_all(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('animales') or []
        import datetime
        for d in data:
            a = Animal.from_dict(d)
            self._animales[a.id] = a
            self._next = max(self._next, a.id+1)

    def marcar_cuarentena(self, animal_id: int, fecha_fin=None, motivo: str = None):
        a = self._animales.get(animal_id)
        if not a:
            raise ValueError("Animal no encontrado")
        a.estado = 'cuarentena'
        # store quarantine metadata if service attached
        if self._quarantine_service:
            from datetime import date
            inicio = date.today()
            fin = fecha_fin
            self._quarantine_service.marcar(animal_id, fecha_inicio=inicio, fecha_fin=fin, motivo=motivo)
        # persist animals if service available
        self.persist_all()
        return {"animal_id": animal_id, "estado": "cuarentena", "fecha_fin": fecha_fin.isoformat() if fecha_fin else None, "motivo": motivo}

    def attach_quarantine_service(self, svc):
        self._quarantine_service = svc
