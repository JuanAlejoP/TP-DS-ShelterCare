from abc import ABC, abstractmethod
from datetime import date
from src.entidades.animal import Animal

class AlimentacionStrategy(ABC):
    @abstractmethod
    def calcular_racion(self, animal: "Animal", fecha: date) -> float:
        """Calcula la ración recomendada para el animal en la fecha dada.
        Implementaciones concretas deben sobrescribir este método.
        """
        raise NotImplementedError()

class PorPesoStrategy(AlimentacionStrategy):
    def calcular_racion(self, animal, fecha):
        from src.constantes import RACION_POR_KG_PERRO, RACION_POR_KG_GATO
        from src.entidades.perro import Perro
        from src.entidades.gato import Gato
        if isinstance(animal, Perro):
            return animal.peso_kg * RACION_POR_KG_PERRO
        if isinstance(animal, Gato):
            return animal.peso_kg * RACION_POR_KG_GATO
        # fallback
        return max(0.05, animal.peso_kg * 0.02)
