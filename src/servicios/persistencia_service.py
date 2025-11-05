import json
import os
import tempfile
from typing import Any

class PersistenciaService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def _path(self, name: str) -> str:
        return os.path.join(self.data_dir, f"{name}.json")

    def save(self, name: str, obj: Any) -> None:
        path = self._path(name)
        fd, tmp = tempfile.mkstemp(dir=self.data_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    def load(self, name: str):
        path = self._path(name)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_files(self):
        return [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
