import datetime
from typing import Dict, List

class QuarantineService:
    def __init__(self, persistencia=None):
        # animal_id -> {fecha_inicio, fecha_fin, motivo}
        self._cuarentenas: Dict[int, dict] = {}
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('cuarentenas') or {}
        self._cuarentenas = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._cuarentenas.items()}
        self.persistencia.save('cuarentenas', data)

    def marcar(self, animal_id: int, fecha_inicio: datetime.date = None, fecha_fin: datetime.date = None, motivo: str = None):
        fecha_inicio = fecha_inicio or datetime.date.today()
        entry = {"fecha_inicio": fecha_inicio.isoformat(), "fecha_fin": fecha_fin.isoformat() if fecha_fin else None, "motivo": motivo}
        self._cuarentenas[animal_id] = entry
        self._save()
        return entry

    def quitar(self, animal_id: int):
        if animal_id in self._cuarentenas:
            del self._cuarentenas[animal_id]
            self._save()
            return True
        return False

    def esta_en_cuarentena(self, animal_id: int) -> bool:
        entry = self._cuarentenas.get(animal_id)
        if not entry:
            return False
        if entry.get('fecha_fin'):
            fecha_fin = datetime.date.fromisoformat(entry['fecha_fin'])
            if datetime.date.today() > fecha_fin:
                # expired
                return False
        return True

    def get(self, animal_id: int):
        return self._cuarentenas.get(animal_id)
