import threading
import time
import random
from src.patrones.observer.observable import Observable

class SimuladorSensoresService:
    def __init__(self, observable: Observable = None):
        self.observable = observable or Observable()
        self._threads = []
        self._running = False

    def simular(self, cantidad_sensores: int = 10, duracion_seg: int = 10, probabilidad_pico: float = 0.05):
        events = []
        self._running = True
        def sensor_thread(i):
            t0 = time.time()
            while time.time() - t0 < duracion_seg:
                time.sleep(random.uniform(0.1, 0.5))
                valor = random.uniform(10.0, 40.0)
                if random.random() < probabilidad_pico:
                    valor = random.uniform(0.0, 5.0) if random.random()<0.5 else random.uniform(45.0, 80.0)
                evento = {"sensor_id": i, "valor": valor, "ts": time.time()}
                events.append(evento)
                try:
                    self.observable.notificar_observadores(evento)
                except Exception:
                    pass
        threads = []
        for i in range(cantidad_sensores):
            t = threading.Thread(target=sensor_thread, args=(i,), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        self._running = False
        return events
