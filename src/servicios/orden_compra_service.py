from typing import List, Dict

class OrdenCompraService:
    def __init__(self, persistencia=None):
        self._ordenes: List[Dict] = []
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('ordenes') or []
        self._ordenes = data

    def _save(self):
        if not self.persistencia:
            return
        self.persistencia.save('ordenes', self._ordenes)

    def crear_orden(self, items: List[Dict], proveedor: str = None) -> Dict:
        orden = {"id": len(self._ordenes) + 1, "items": items, "proveedor": proveedor, "estado": "pendiente"}
        self._ordenes.append(orden)
        self._save()
        return orden

    def list_ordenes(self):
        return list(self._ordenes)
