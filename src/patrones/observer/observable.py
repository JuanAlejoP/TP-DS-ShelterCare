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
