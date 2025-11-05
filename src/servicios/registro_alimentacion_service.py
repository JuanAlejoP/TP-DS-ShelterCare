import datetime
from typing import Dict, List

class RegistroAlimentacionService:
    def __init__(self, persistencia=None):
        self._registros: Dict[int, List[dict]] = {}  # animal_id -> list
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('alimentaciones') or {}
        self._registros = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._registros.items()}
        self.persistencia.save('alimentaciones', data)

    def registrar(self, animal_id:int, quien:str, cantidad:float, fecha=None, observaciones:str=None):
        fecha = fecha or datetime.datetime.now().isoformat()
        entry = {"fecha": fecha, "quien": quien, "cantidad": cantidad, "observaciones": observaciones}
        self._registros.setdefault(animal_id, []).append(entry)
        self._save()
        return entry

    def historial_por_animal(self, animal_id:int):
        return self._registros.get(animal_id, [])
