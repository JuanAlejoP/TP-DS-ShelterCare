from typing import Dict, List
import datetime

class VacunaService:
    def __init__(self, persistencia=None):
        self._vacunas: Dict[int, List[dict]] = {}  # animal_id -> list of vacunas
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('vacunas') or {}
        # data expected: {str(animal_id): [vacs]}
        self._vacunas = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._vacunas.items()}
        self.persistencia.save('vacunas', data)

    def registrar_vacuna(self, animal_id: int, vacuna: str, lote: str, fecha: datetime.date, veterinario_id: int, proximo_refuerzo: datetime.date = None):
        entry = {"vacuna": vacuna, "lote": lote, "fecha": fecha.isoformat(), "veterinario_id": veterinario_id, "proximo_refuerzo": proximo_refuerzo.isoformat() if proximo_refuerzo else None}
        self._vacunas.setdefault(animal_id, []).append(entry)
        self._save()
        return entry

    def listar_vacunas(self, animal_id: int):
        return self._vacunas.get(animal_id, [])

    def animales_con_refuerzo_proximo(self, dias: int = 7):
        resultado = []
        hoy = datetime.date.today()
        for aid, vacs in self._vacunas.items():
            for v in vacs:
                if v.get('proximo_refuerzo'):
                    pr = datetime.date.fromisoformat(v['proximo_refuerzo'])
                    if 0 <= (pr - hoy).days <= dias:
                        resultado.append({"animal_id": aid, **v})
        return resultado

    def enviar_recordatorios(self, notificacion_service, dias:int=7):
        proximos = self.animales_con_refuerzo_proximo(dias=dias)
        for p in proximos:
            # notification placeholder: destino could be owner email in a richer model
            notificacion_service.enviar(destino="admin@refugio.local", asunto="Recordatorio vacuna", mensaje=f"Animal {p['animal_id']} tiene refuerzo próximo el {p['proximo_refuerzo']}")
        return len(proximos)
