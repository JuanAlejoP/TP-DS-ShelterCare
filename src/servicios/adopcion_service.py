from typing import Dict
import datetime

class AdopcionService:
    def __init__(self, persistencia=None):
        self._solicitudes: Dict[int, dict] = {}
        self._next = 1
        self.persistencia = persistencia
        self._load()
        self._postadop_service = None

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('adopciones') or []
        for s in data:
            self._solicitudes[s['id']] = s
        if self._solicitudes:
            self._next = max(self._solicitudes.keys()) + 1

    def _save(self):
        if not self.persistencia:
            return
        self.persistencia.save('adopciones', list(self._solicitudes.values()))

    def crear_solicitud(self, datos: dict) -> dict:
        datos_entry = dict(datos)
        datos_entry.update({"id": self._next, "estado": "pendiente", "fecha": datetime.date.today().isoformat()})
        # if the solicitud references an animal, check quarantine and mark a field
        animal_id = datos_entry.get('animal_id')
        if animal_id and self.persistencia:
            # try to load animal state via provided animal_service later at evaluation; store request as-is
            pass
        self._solicitudes[self._next] = datos_entry
        self._next += 1
        self._save()
        return datos_entry

    def evaluar_solicitud(self, solicitud_id: int, aprobado: bool, motivo: str = None, animal_id: int = None, animal_service=None):
        s = self._solicitudes.get(solicitud_id)
        if not s:
            raise ValueError("Solicitud no encontrada")
        # if animal_id provided, check animal not in cuarentena
        if animal_id and animal_service:
            a = animal_service.get(animal_id)
            # prefer quarantine service if attached
            in_cuarentena = False
            if a and getattr(a, 'estado', None) == 'cuarentena':
                in_cuarentena = True
            # if animal_service has quarantine service attached, check it
            try:
                qs = getattr(animal_service, '_quarantine_service', None)
                if qs and qs.esta_en_cuarentena(animal_id):
                    in_cuarentena = True
            except Exception:
                pass
            if in_cuarentena and aprobado:
                raise ValueError("No se puede aprobar adopción: animal en cuarentena")
            s['animal_id'] = animal_id
        s["estado"] = "aprobada" if aprobado else "rechazada"
        s["motivo"] = motivo
        # if approved, trigger post-adoption scheduling when service attached
        if aprobado and self._postadop_service:
            self._postadop_service.programar_seguimientos(solicitud_id)
        self._save()
        return s

    def attach_postadop_service(self, svc):
        self._postadop_service = svc
