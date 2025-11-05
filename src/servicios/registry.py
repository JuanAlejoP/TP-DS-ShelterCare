import threading

class ShelterServiceRegistry:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_registry()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def _init_registry(self):
        self._services = {}

    def register(self, name: str, svc) -> None:
        self._services[name] = svc

    def get(self, name: str):
        return self._services.get(name)
