from typing import Dict, Any
from src.servicios.registry import ShelterServiceRegistry
import datetime

class ReportesService:
    def __init__(self, registry: ShelterServiceRegistry):
        self.registry = registry

    def reporte_ocupacion(self) -> Dict[str, Any]:
        sede = self.registry.get('sede')
        if not sede:
            return {"ocupacion": None}
        zonas = [{"nombre": z.nombre, "capacidad": z.capacidad, "ocupacion": z.ocupacion} for z in sede.zonas]
        total = sum(z['ocupacion'] for z in zonas)
        return {"zonas": zonas, "total_ocupacion": total, "capacidad_total": sede.capacidad_total}

    def reporte_vacunas_periodo(self, dias:int=30):
        vac_svc = self.registry.get('vacunas')
        if not vac_svc:
            return []
        hoy = datetime.date.today()
        res = []
        for aid, vacs in vac_svc._vacunas.items():
            for v in vacs:
                fecha = datetime.date.fromisoformat(v['fecha'])
                if (hoy - fecha).days <= dias:
                    res.append({"animal_id": aid, **v})
        return res

    def reporte_adopciones_por_mes(self):
        adop_svc = self.registry.get('adopcion')
        if not adop_svc:
            return {}
        # compute counts by YYYY-MM
        counts = {}
        for s in adop_svc._solicitudes.values():
            fecha = s.get('fecha')
            if fecha:
                key = fecha[:7]
                counts[key] = counts.get(key, 0) + 1
        return counts
