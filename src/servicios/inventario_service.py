from threading import Lock
from typing import Dict
from src.entidades.inventario import ProductoInventario

class InventarioService:
    def __init__(self):
        self._items: Dict[str, ProductoInventario] = {}
        self._locks: Dict[str, Lock] = {}
        self.persistencia = None

    def add_item(self, producto: ProductoInventario):
        self._items[producto.sku] = producto
        self._locks[producto.sku] = Lock()
        # persist if configured
        if self.persistencia:
            self._save()

    def _save(self):
        if not self.persistencia:
            return
        data = [p.to_dict() for p in self._items.values()]
        self.persistencia.save('inventario', data)

    def load_all(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('inventario') or []
        for d in data:
            p = ProductoInventario.from_dict(d)
            self._items[p.sku] = p
            self._locks[p.sku] = Lock()

    def get(self, sku: str):
        return self._items.get(sku)

    def decrementar_stock(self, sku: str, cantidad: int) -> None:
        if sku not in self._items:
            raise ValueError("SKU desconocido")
        lock = self._locks[sku]
        with lock:
            item = self._items[sku]
            if item.cantidad < cantidad:
                raise ValueError("InventarioInsuficienteException")
            item.cantidad -= cantidad

    def incrementar_stock(self, sku: str, cantidad: int) -> None:
        if sku not in self._items:
            raise ValueError("SKU desconocido")
        lock = self._locks[sku]
        with lock:
            item = self._items[sku]
            item.cantidad += cantidad

    def list_items(self):
        return list(self._items.values())

    def check_reorden(self):
        suggestions = []
        for sku, item in self._items.items():
            if item.cantidad <= item.punto_reorden:
                suggestions.append({"sku": sku, "nombre": item.nombre, "cantidad_actual": item.cantidad, "sugerido": max(item.punto_reorden * 2 - item.cantidad, 1)})
        return suggestions
