from src.entidades.historia_medica import HistoriaMedica, Examen
from src.servicios.inventario_service import InventarioService
from typing import Dict

class MedicinaService:
    def __init__(self, inventario: InventarioService = None):
        self._historias: Dict[int, HistoriaMedica] = {}
        self.inventario = inventario

    def registrar_examen(self, animal_id: int, vet_id: int, hallazgos: str, diagnostico: str, prescripcion: list):
        from datetime import date
        examen = Examen(fecha=date.today(), veterinario_id=vet_id, hallazgos=hallazgos, diagnostico=diagnostico, prescripcion=prescripcion)
        hist = self._historias.get(animal_id)
        if not hist:
            hist = HistoriaMedica(animal_id=animal_id)
            self._historias[animal_id] = hist
        hist.examenes.append(examen)
        # decrementar inventario por prescripcion
        if self.inventario:
            for item in prescripcion:
                sku = item.get('medicamento')
                cantidad = item.get('cantidad', 1)
                try:
                    self.inventario.decrementar_stock(sku, cantidad)
                except Exception:
                    # en este MVP solo registramos la falta
                    pass
        return examen

    def get_historia(self, animal_id: int):
        return self._historias.get(animal_id)
