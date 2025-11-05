from typing import Dict
from src.patrones.strategy.alimentacion import AlimentacionStrategy, PorPesoStrategy

class AlimentacionService:
    def __init__(self):
        # strategy por animal id
        self._strategies: Dict[int, AlimentacionStrategy] = {}
        self.persistencia = None
        self._registro_service = None

    def set_strategy(self, animal_id: int, strategy: AlimentacionStrategy) -> None:
        self._strategies[animal_id] = strategy

    def calcular_racion(self, animal, fecha=None) -> float:
        fecha = fecha
        strat = self._strategies.get(animal.id)
        if not strat:
            strat = PorPesoStrategy()
        return strat.calcular_racion(animal, fecha)

    def registrar_alimentacion(self, animal_id: int, cantidad: float, quien: str):
        entry = {"animal_id": animal_id, "cantidad": cantidad, "quien": quien}
        if self._registro_service:
            self._registro_service.registrar(animal_id, quien, cantidad)
        return entry

    def attach_registro_service(self, registro_service):
        self._registro_service = registro_service
