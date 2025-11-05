"""
Archivo integrador generado automaticamente
Directorio: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/patrones/observer
Fecha: 2025-11-05 03:19:09
Total de archivos integrados: 1
"""

# ================================================================================
# ARCHIVO 1/1: observable.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/patrones/observer/observable.py
# ================================================================================

from typing import Generic, TypeVar, List, Protocol

T = TypeVar("T")

class Observer(Protocol[T]):
    def actualizar(self, evento: T) -> None: ...

class Observable(Generic[T]):
    def __init__(self):
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, o: Observer[T]) -> None:
        self._observadores.append(o)

    def quitar_observador(self, o: Observer[T]) -> None:
        try:
            self._observadores.remove(o)
        except ValueError:
            pass

    def notificar_observadores(self, evento: T) -> None:
        for o in list(self._observadores):
            try:
                o.actualizar(evento)
            except Exception:
                # no dejar que un observer rompa la cadena
                pass


