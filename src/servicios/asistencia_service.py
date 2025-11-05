import datetime
from typing import Dict, List

class AsistenciaService:
    def __init__(self, persistencia=None):
        # registros: persona_id -> list of {in, out}
        self._registros: Dict[int, List[dict]] = {}
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('asistencias') or {}
        self._registros = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._registros.items()}
        self.persistencia.save('asistencias', data)

    def fichar_entrada(self, persona_id:int, ts:datetime.datetime=None):
        ts = ts or datetime.datetime.now()
        self._registros.setdefault(persona_id, []).append({"in": ts.isoformat(), "out": None})
        self._save()
        return self._registros[persona_id][-1]

    def fichar_salida(self, persona_id:int, ts:datetime.datetime=None):
        ts = ts or datetime.datetime.now()
        regs = self._registros.get(persona_id)
        if not regs or regs[-1].get('out') is not None:
            raise ValueError("No hay entrada abierta para esta persona")
        regs[-1]['out'] = ts.isoformat()
        self._save()
        return regs[-1]

    def horas_por_periodo(self, persona_id:int, desde:datetime.date, hasta:datetime.date):
        regs = self._registros.get(persona_id, [])
        total = 0.0
        for r in regs:
            if r.get('out'):
                tin = datetime.datetime.fromisoformat(r['in'])
                tout = datetime.datetime.fromisoformat(r['out'])
                if desde <= tin.date() <= hasta:
                    total += (tout - tin).total_seconds() / 3600.0
        return total
