import datetime
from typing import Dict, List

class PostAdopcionService:
    def __init__(self, persistencia=None):
        # adopcion_id -> list of seguimientos {fecha_programada, estado, respuesta, escalado}
        self._seguimientos: Dict[int, List[dict]] = {}
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('postadopcion') or {}
        self._seguimientos = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._seguimientos.items()}
        self.persistencia.save('postadopcion', data)

    def programar_seguimientos(self, adopcion_id: int):
        dias = [7, 30, 90]
        hoy = datetime.date.today()
        lista = []
        for d in dias:
            lista.append({"fecha_programada": (hoy + datetime.timedelta(days=d)).isoformat(), "estado": "pendiente", "respuesta": None, "escalado": False})
        self._seguimientos[adopcion_id] = lista
        self._save()
        return lista

    def registrar_respuesta(self, adopcion_id: int, fecha_programada: str, respuesta: str):
        segs = self._seguimientos.get(adopcion_id)
        if not segs:
            raise ValueError("Seguimientos no encontrados")
        for s in segs:
            if s['fecha_programada'] == fecha_programada:
                s['estado'] = 'respondido'
                s['respuesta'] = respuesta
                s['escalado'] = False
                self._save()
                return s
        raise ValueError("Seguimiento no encontrado para la fecha dada")

    def evaluar_respuestas_y_escalar(self, dias_sin_respuesta:int=7):
        # simple: marca como escalado los seguimientos pendientes que exceden dias_sin_respuesta desde fecha_programada
        hoy = datetime.date.today()
        escalados = []
        for aid, segs in self._seguimientos.items():
            for s in segs:
                if s['estado'] == 'pendiente':
                    fp = datetime.date.fromisoformat(s['fecha_programada'])
                    if (hoy - fp).days > dias_sin_respuesta:
                        s['escalado'] = True
                        escalados.append({"adopcion_id": aid, "fecha": s['fecha_programada']})
        if escalados:
            self._save()
        return escalados

    def get_seguimientos(self, adopcion_id:int):
        return self._seguimientos.get(adopcion_id, [])
