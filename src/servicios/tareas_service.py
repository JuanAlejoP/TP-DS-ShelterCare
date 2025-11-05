import datetime
from typing import Dict, List

class TareasService:
    def __init__(self, persistencia=None):
        self._tareas: Dict[int, dict] = {}
        self._next = 1
        self.persistencia = persistencia
        self._load()
        self.max_tasks_per_person = 3

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('tareas') or []
        for t in data:
            self._tareas[t['id']] = t
        self._next = max(self._tareas.keys(), default=0) + 1

    def _save(self):
        if not self.persistencia:
            return
        self.persistencia.save('tareas', list(self._tareas.values()))

    def crear_tarea(self, descripcion: str, prioridad:int=1, duracion_estim:int=30, asignados:List[int]=None, fecha_programada: str = None):
        t = {"id": self._next, "descripcion": descripcion, "prioridad": prioridad, "duracion_estimada": duracion_estim, "asignados": asignados or [], "fecha_programada": fecha_programada, "estado": "pendiente"}
        self._tareas[self._next] = t
        self._next += 1
        self._save()
        return t

    def asignar(self, tarea_id:int, persona_id:int):
        t = self._tareas.get(tarea_id)
        if not t:
            raise ValueError("Tarea no encontrada")
        # enforce max tasks per person
        asignados_count = sum(1 for x in self._tareas.values() if persona_id in x.get('asignados', []) and x.get('estado') != 'completada')
        if asignados_count >= self.max_tasks_per_person:
            raise ValueError(f"La persona {persona_id} tiene el máximo de tareas asignadas ({self.max_tasks_per_person})")
        if persona_id not in t['asignados']:
            t['asignados'].append(persona_id)
        self._save()
        return t

    def marcar_completada(self, tarea_id:int):
        t = self._tareas.get(tarea_id)
        if not t:
            raise ValueError("Tarea no encontrada")
        t['estado'] = 'completada'
        self._save()
        return t

    def list_tareas(self):
        return list(self._tareas.values())
