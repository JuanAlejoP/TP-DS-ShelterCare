from dataclasses import dataclass

@dataclass
class ProductoInventario:
    sku: str
    nombre: str
    categoria: str
    cantidad: int
    unidad: str
    punto_reorden: int = 10

    def to_dict(self):
        return {"sku": self.sku, "nombre": self.nombre, "categoria": self.categoria, "cantidad": self.cantidad, "unidad": self.unidad, "punto_reorden": self.punto_reorden}

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
