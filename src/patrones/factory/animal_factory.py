from typing import Dict, Callable
from src.entidades.animal import Animal
from src.entidades.perro import Perro
from src.entidades.gato import Gato
import datetime

class AnimalFactory:
    _map: Dict[str, Callable[..., Animal]] = {
        "Dog": lambda **kwargs: Perro(**kwargs),
        "Cat": lambda **kwargs: Gato(**kwargs),
    }

    @staticmethod
    def crear_animal(especie: str, **kwargs) -> Animal:
        especie = especie if especie in AnimalFactory._map else especie.title()
        if especie not in AnimalFactory._map:
            raise ValueError(f"Especie desconocida: {especie}")
        # Ensure fecha_ingreso present
        if "fecha_ingreso" not in kwargs:
            kwargs["fecha_ingreso"] = datetime.date.today()
        return AnimalFactory._map[especie](**kwargs)
