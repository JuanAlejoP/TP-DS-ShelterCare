"""
Archivo integrador generado automaticamente
Directorio: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios
Fecha: 2025-11-05 03:19:09
Total de archivos integrados: 21
"""

# ================================================================================
# ARCHIVO 1/21: adopcion_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/adopcion_service.py
# ================================================================================

from typing import Dict
import datetime

class AdopcionService:
    def __init__(self, persistencia=None):
        self._solicitudes: Dict[int, dict] = {}
        self._next = 1
        self.persistencia = persistencia
        self._load()
        self._postadop_service = None

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('adopciones') or []
        for s in data:
            self._solicitudes[s['id']] = s
        if self._solicitudes:
            self._next = max(self._solicitudes.keys()) + 1

    def _save(self):
        if not self.persistencia:
            return
        self.persistencia.save('adopciones', list(self._solicitudes.values()))

    def crear_solicitud(self, datos: dict) -> dict:
        datos_entry = dict(datos)
        datos_entry.update({"id": self._next, "estado": "pendiente", "fecha": datetime.date.today().isoformat()})
        # if the solicitud references an animal, check quarantine and mark a field
        animal_id = datos_entry.get('animal_id')
        if animal_id and self.persistencia:
            # try to load animal state via provided animal_service later at evaluation; store request as-is
            pass
        self._solicitudes[self._next] = datos_entry
        self._next += 1
        self._save()
        return datos_entry

    def evaluar_solicitud(self, solicitud_id: int, aprobado: bool, motivo: str = None, animal_id: int = None, animal_service=None):
        s = self._solicitudes.get(solicitud_id)
        if not s:
            raise ValueError("Solicitud no encontrada")
        # if animal_id provided, check animal not in cuarentena
        if animal_id and animal_service:
            a = animal_service.get(animal_id)
            # prefer quarantine service if attached
            in_cuarentena = False
            if a and getattr(a, 'estado', None) == 'cuarentena':
                in_cuarentena = True
            # if animal_service has quarantine service attached, check it
            try:
                qs = getattr(animal_service, '_quarantine_service', None)
                if qs and qs.esta_en_cuarentena(animal_id):
                    in_cuarentena = True
            except Exception:
                pass
            if in_cuarentena and aprobado:
                raise ValueError("No se puede aprobar adopción: animal en cuarentena")
            s['animal_id'] = animal_id
        s["estado"] = "aprobada" if aprobado else "rechazada"
        s["motivo"] = motivo
        # if approved, trigger post-adoption scheduling when service attached
        if aprobado and self._postadop_service:
            self._postadop_service.programar_seguimientos(solicitud_id)
        self._save()
        return s

    def attach_postadop_service(self, svc):
        self._postadop_service = svc


# ================================================================================
# ARCHIVO 2/21: alarma_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/alarma_service.py
# ================================================================================

from src.patrones.observer.observable import Observer

class AlarmaService(Observer):
    def __init__(self):
        self.alerts = []

    def actualizar(self, evento):
        # evento: {sensor_id, valor, ts}
        v = evento.get('valor')
        if v < 12.0 or v > 40.0:
            alert = {"sensor_id": evento.get('sensor_id'), "valor": v, "ts": evento.get('ts')}
            self.alerts.append(alert)
            print(f"ALERTA: sensor {alert['sensor_id']} valor {alert['valor']}")


# ================================================================================
# ARCHIVO 3/21: alimentacion_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/alimentacion_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/21: animal_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/animal_service.py
# ================================================================================

from typing import Dict
from src.entidades.animal import Animal
from src.patrones.factory.animal_factory import AnimalFactory
import datetime

class AnimalService:
    def __init__(self, persistencia=None):
        self._animales: Dict[int, Animal] = {}
        self._next = 1
        self.persistencia = persistencia
        self._quarantine_service = None

    def ingresar_animal(self, especie: str, nombre: str = None, edad_meses: int = 0, sexo: str = 'U', zona: str = None, peso_kg: float = 0.0):
        a = AnimalFactory.crear_animal(especie, id=self._next, nombre=nombre, edad_meses=edad_meses, sexo=sexo, fecha_ingreso=datetime.date.today(), zona=zona, peso_kg=peso_kg)
        self._animales[self._next] = a
        self._next += 1
        return a

    def get(self, aid: int) -> Animal:
        return self._animales.get(aid)

    def list_all(self):
        return list(self._animales.values())

    def persist_all(self):
        if not self.persistencia:
            return
        data = [a.to_dict() for a in self._animales.values()]
        self.persistencia.save('animales', data)

    def load_all(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('animales') or []
        import datetime
        for d in data:
            a = Animal.from_dict(d)
            self._animales[a.id] = a
            self._next = max(self._next, a.id+1)

    def marcar_cuarentena(self, animal_id: int, fecha_fin=None, motivo: str = None):
        a = self._animales.get(animal_id)
        if not a:
            raise ValueError("Animal no encontrado")
        a.estado = 'cuarentena'
        # store quarantine metadata if service attached
        if self._quarantine_service:
            from datetime import date
            inicio = date.today()
            fin = fecha_fin
            self._quarantine_service.marcar(animal_id, fecha_inicio=inicio, fecha_fin=fin, motivo=motivo)
        # persist animals if service available
        self.persist_all()
        return {"animal_id": animal_id, "estado": "cuarentena", "fecha_fin": fecha_fin.isoformat() if fecha_fin else None, "motivo": motivo}

    def attach_quarantine_service(self, svc):
        self._quarantine_service = svc


# ================================================================================
# ARCHIVO 5/21: asistencia_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/asistencia_service.py
# ================================================================================

import datetime
from typing import Dict, List

class AsistenciaService:
    def __init__(self, persistencia=None):
        # registros: persona_id -> list of {in, out}
        self._registros: Dict[int, List[dict]] = {}
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('asistencias') or {}
        self._registros = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._registros.items()}
        self.persistencia.save('asistencias', data)

    def fichar_entrada(self, persona_id:int, ts:datetime.datetime=None):
        ts = ts or datetime.datetime.now()
        self._registros.setdefault(persona_id, []).append({"in": ts.isoformat(), "out": None})
        self._save()
        return self._registros[persona_id][-1]

    def fichar_salida(self, persona_id:int, ts:datetime.datetime=None):
        ts = ts or datetime.datetime.now()
        regs = self._registros.get(persona_id)
        if not regs or regs[-1].get('out') is not None:
            raise ValueError("No hay entrada abierta para esta persona")
        regs[-1]['out'] = ts.isoformat()
        self._save()
        return regs[-1]

    def horas_por_periodo(self, persona_id:int, desde:datetime.date, hasta:datetime.date):
        regs = self._registros.get(persona_id, [])
        total = 0.0
        for r in regs:
            if r.get('out'):
                tin = datetime.datetime.fromisoformat(r['in'])
                tout = datetime.datetime.fromisoformat(r['out'])
                if desde <= tin.date() <= hasta:
                    total += (tout - tin).total_seconds() / 3600.0
        return total


# ================================================================================
# ARCHIVO 6/21: inventario_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/inventario_service.py
# ================================================================================

from threading import Lock
from typing import Dict
from src.entidades.inventario import ProductoInventario

class InventarioService:
    def __init__(self):
        self._items: Dict[str, ProductoInventario] = {}
        self._locks: Dict[str, Lock] = {}
        self.persistencia = None

    def add_item(self, producto: ProductoInventario):
        self._items[producto.sku] = producto
        self._locks[producto.sku] = Lock()
        # persist if configured
        if self.persistencia:
            self._save()

    def _save(self):
        if not self.persistencia:
            return
        data = [p.to_dict() for p in self._items.values()]
        self.persistencia.save('inventario', data)

    def load_all(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('inventario') or []
        for d in data:
            p = ProductoInventario.from_dict(d)
            self._items[p.sku] = p
            self._locks[p.sku] = Lock()

    def get(self, sku: str):
        return self._items.get(sku)

    def decrementar_stock(self, sku: str, cantidad: int) -> None:
        if sku not in self._items:
            raise ValueError("SKU desconocido")
        lock = self._locks[sku]
        with lock:
            item = self._items[sku]
            if item.cantidad < cantidad:
                raise ValueError("InventarioInsuficienteException")
            item.cantidad -= cantidad

    def incrementar_stock(self, sku: str, cantidad: int) -> None:
        if sku not in self._items:
            raise ValueError("SKU desconocido")
        lock = self._locks[sku]
        with lock:
            item = self._items[sku]
            item.cantidad += cantidad

    def list_items(self):
        return list(self._items.values())

    def check_reorden(self):
        suggestions = []
        for sku, item in self._items.items():
            if item.cantidad <= item.punto_reorden:
                suggestions.append({"sku": sku, "nombre": item.nombre, "cantidad_actual": item.cantidad, "sugerido": max(item.punto_reorden * 2 - item.cantidad, 1)})
        return suggestions


# ================================================================================
# ARCHIVO 7/21: medicina_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/medicina_service.py
# ================================================================================

from src.entidades.historia_medica import HistoriaMedica, Examen
from src.servicios.inventario_service import InventarioService
from typing import Dict

class MedicinaService:
    def __init__(self, inventario: InventarioService = None):
        self._historias: Dict[int, HistoriaMedica] = {}
        self.inventario = inventario

    def registrar_examen(self, animal_id: int, vet_id: int, hallazgos: str, diagnostico: str, prescripcion: list):
        from datetime import date
        examen = Examen(fecha=date.today(), veterinario_id=vet_id, hallazgos=hallazgos, diagnostico=diagnostico, prescripcion=prescripcion)
        hist = self._historias.get(animal_id)
        if not hist:
            hist = HistoriaMedica(animal_id=animal_id)
            self._historias[animal_id] = hist
        hist.examenes.append(examen)
        # decrementar inventario por prescripcion
        if self.inventario:
            for item in prescripcion:
                sku = item.get('medicamento')
                cantidad = item.get('cantidad', 1)
                try:
                    self.inventario.decrementar_stock(sku, cantidad)
                except Exception:
                    # en este MVP solo registramos la falta
                    pass
        return examen

    def get_historia(self, animal_id: int):
        return self._historias.get(animal_id)


# ================================================================================
# ARCHIVO 8/21: notificacion_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/notificacion_service.py
# ================================================================================

class NotificacionService:
    def __init__(self):
        pass

    def enviar(self, destino: str, asunto: str, mensaje: str):
        # placeholder: print to console
        print(f"NOTIFICACIÓN a {destino}: {asunto} - {mensaje}")


# ================================================================================
# ARCHIVO 9/21: orden_compra_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/orden_compra_service.py
# ================================================================================

from typing import List, Dict

class OrdenCompraService:
    def __init__(self, persistencia=None):
        self._ordenes: List[Dict] = []
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('ordenes') or []
        self._ordenes = data

    def _save(self):
        if not self.persistencia:
            return
        self.persistencia.save('ordenes', self._ordenes)

    def crear_orden(self, items: List[Dict], proveedor: str = None) -> Dict:
        orden = {"id": len(self._ordenes) + 1, "items": items, "proveedor": proveedor, "estado": "pendiente"}
        self._ordenes.append(orden)
        self._save()
        return orden

    def list_ordenes(self):
        return list(self._ordenes)


# ================================================================================
# ARCHIVO 10/21: persistencia_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/persistencia_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 11/21: personal_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/personal_service.py
# ================================================================================

from typing import Dict
from src.entidades.personal import Personal
import datetime

class PersonalService:
    def __init__(self):
        self._personas: Dict[int, Personal] = {}
        self._next = 1
        self.persistencia = None

        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('personal') or []
        import datetime
        for d in data:
            p = Personal.from_dict(d)
            self._personas[p.id] = p
            self._next = max(self._next, p.id+1)

    def _save(self):
        if not self.persistencia:
            return
        data = [p.to_dict() for p in self._personas.values()]
        self.persistencia.save('personal', data)

    def crear_personal(self, nombre: str, rol: str, contacto: dict, fecha_alta=None) -> Personal:
        fecha_alta = fecha_alta or datetime.date.today()
        p = Personal(id=self._next, nombre=nombre, rol=rol, contacto=contacto, fecha_alta=fecha_alta)
        self._personas[self._next] = p
        self._next += 1
        self._save()
        return p

    def get(self, pid: int) -> Personal:
        return self._personas.get(pid)

    def list_all(self):
        return list(self._personas.values())


# ================================================================================
# ARCHIVO 12/21: postadopcion_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/postadopcion_service.py
# ================================================================================

import datetime
from typing import Dict, List

class PostAdopcionService:
    def __init__(self, persistencia=None):
        # adopcion_id -> list of seguimientos {fecha_programada, estado, respuesta, escalado}
        self._seguimientos: Dict[int, List[dict]] = {}
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('postadopcion') or {}
        self._seguimientos = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._seguimientos.items()}
        self.persistencia.save('postadopcion', data)

    def programar_seguimientos(self, adopcion_id: int):
        dias = [7, 30, 90]
        hoy = datetime.date.today()
        lista = []
        for d in dias:
            lista.append({"fecha_programada": (hoy + datetime.timedelta(days=d)).isoformat(), "estado": "pendiente", "respuesta": None, "escalado": False})
        self._seguimientos[adopcion_id] = lista
        self._save()
        return lista

    def registrar_respuesta(self, adopcion_id: int, fecha_programada: str, respuesta: str):
        segs = self._seguimientos.get(adopcion_id)
        if not segs:
            raise ValueError("Seguimientos no encontrados")
        for s in segs:
            if s['fecha_programada'] == fecha_programada:
                s['estado'] = 'respondido'
                s['respuesta'] = respuesta
                s['escalado'] = False
                self._save()
                return s
        raise ValueError("Seguimiento no encontrado para la fecha dada")

    def evaluar_respuestas_y_escalar(self, dias_sin_respuesta:int=7):
        # simple: marca como escalado los seguimientos pendientes que exceden dias_sin_respuesta desde fecha_programada
        hoy = datetime.date.today()
        escalados = []
        for aid, segs in self._seguimientos.items():
            for s in segs:
                if s['estado'] == 'pendiente':
                    fp = datetime.date.fromisoformat(s['fecha_programada'])
                    if (hoy - fp).days > dias_sin_respuesta:
                        s['escalado'] = True
                        escalados.append({"adopcion_id": aid, "fecha": s['fecha_programada']})
        if escalados:
            self._save()
        return escalados

    def get_seguimientos(self, adopcion_id:int):
        return self._seguimientos.get(adopcion_id, [])


# ================================================================================
# ARCHIVO 13/21: quarantine_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/quarantine_service.py
# ================================================================================

import datetime
from typing import Dict, List

class QuarantineService:
    def __init__(self, persistencia=None):
        # animal_id -> {fecha_inicio, fecha_fin, motivo}
        self._cuarentenas: Dict[int, dict] = {}
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('cuarentenas') or {}
        self._cuarentenas = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._cuarentenas.items()}
        self.persistencia.save('cuarentenas', data)

    def marcar(self, animal_id: int, fecha_inicio: datetime.date = None, fecha_fin: datetime.date = None, motivo: str = None):
        fecha_inicio = fecha_inicio or datetime.date.today()
        entry = {"fecha_inicio": fecha_inicio.isoformat(), "fecha_fin": fecha_fin.isoformat() if fecha_fin else None, "motivo": motivo}
        self._cuarentenas[animal_id] = entry
        self._save()
        return entry

    def quitar(self, animal_id: int):
        if animal_id in self._cuarentenas:
            del self._cuarentenas[animal_id]
            self._save()
            return True
        return False

    def esta_en_cuarentena(self, animal_id: int) -> bool:
        entry = self._cuarentenas.get(animal_id)
        if not entry:
            return False
        if entry.get('fecha_fin'):
            fecha_fin = datetime.date.fromisoformat(entry['fecha_fin'])
            if datetime.date.today() > fecha_fin:
                # expired
                return False
        return True

    def get(self, animal_id: int):
        return self._cuarentenas.get(animal_id)


# ================================================================================
# ARCHIVO 14/21: registro_alimentacion_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/registro_alimentacion_service.py
# ================================================================================

import datetime
from typing import Dict, List

class RegistroAlimentacionService:
    def __init__(self, persistencia=None):
        self._registros: Dict[int, List[dict]] = {}  # animal_id -> list
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('alimentaciones') or {}
        self._registros = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._registros.items()}
        self.persistencia.save('alimentaciones', data)

    def registrar(self, animal_id:int, quien:str, cantidad:float, fecha=None, observaciones:str=None):
        fecha = fecha or datetime.datetime.now().isoformat()
        entry = {"fecha": fecha, "quien": quien, "cantidad": cantidad, "observaciones": observaciones}
        self._registros.setdefault(animal_id, []).append(entry)
        self._save()
        return entry

    def historial_por_animal(self, animal_id:int):
        return self._registros.get(animal_id, [])


# ================================================================================
# ARCHIVO 15/21: registry.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/registry.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 16/21: reportes_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/reportes_service.py
# ================================================================================

from typing import Dict, Any
from src.servicios.registry import ShelterServiceRegistry
import datetime

class ReportesService:
    def __init__(self, registry: ShelterServiceRegistry):
        self.registry = registry

    def reporte_ocupacion(self) -> Dict[str, Any]:
        sede = self.registry.get('sede')
        if not sede:
            return {"ocupacion": None}
        zonas = [{"nombre": z.nombre, "capacidad": z.capacidad, "ocupacion": z.ocupacion} for z in sede.zonas]
        total = sum(z['ocupacion'] for z in zonas)
        return {"zonas": zonas, "total_ocupacion": total, "capacidad_total": sede.capacidad_total}

    def reporte_vacunas_periodo(self, dias:int=30):
        vac_svc = self.registry.get('vacunas')
        if not vac_svc:
            return []
        hoy = datetime.date.today()
        res = []
        for aid, vacs in vac_svc._vacunas.items():
            for v in vacs:
                fecha = datetime.date.fromisoformat(v['fecha'])
                if (hoy - fecha).days <= dias:
                    res.append({"animal_id": aid, **v})
        return res

    def reporte_adopciones_por_mes(self):
        adop_svc = self.registry.get('adopcion')
        if not adop_svc:
            return {}
        # compute counts by YYYY-MM
        counts = {}
        for s in adop_svc._solicitudes.values():
            fecha = s.get('fecha')
            if fecha:
                key = fecha[:7]
                counts[key] = counts.get(key, 0) + 1
        return counts


# ================================================================================
# ARCHIVO 17/21: sede_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/sede_service.py
# ================================================================================

from src.entidades.sede import Sede, Zona
from typing import Optional

class SedeService:
    def __init__(self):
        self._sede: Optional[Sede] = None

    def crear_sede(self, nombre: str, direccion: str, capacidad_total: int, zonas: list):
        zonas_obj = [Zona(**z) for z in zonas]
        self._sede = Sede(nombre=nombre, direccion=direccion, capacidad_total=capacidad_total, zonas=zonas_obj)
        return self._sede

    def get_sede(self) -> Optional[Sede]:
        return self._sede

    def ocupar_zona(self, nombre_zona: str) -> None:
        if not self._sede:
            raise ValueError("No hay sede creada")
        for z in self._sede.zonas:
            if z.nombre == nombre_zona:
                if z.ocupacion >= z.capacidad:
                    raise ValueError("Capacidad insuficiente en zona")
                z.ocupacion += 1
                return
        raise ValueError("Zona no encontrada")


# ================================================================================
# ARCHIVO 18/21: simulador_salud.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/simulador_salud.py
# ================================================================================

from datetime import date, timedelta

class SimuladorSaludService:
    def __init__(self, animal_service, alimentacion_service):
        self.animal_service = animal_service
        self.alimentacion_service = alimentacion_service

    def simular(self, animal_id: int, dias: int = 30, frecuencia_alimentacion: int = 2):
        animal = self.animal_service.get(animal_id)
        if not animal:
            raise ValueError("Animal no encontrado")
        logs = []
        for d in range(dias):
            # compute racion diaria (sum of frecuencia feeds)
            racion = self.alimentacion_service.calcular_racion(animal, date.today() + timedelta(days=d))
            # simplistic model: peso cambia por 10% of racion/100
            delta = (racion * frecuencia_alimentacion) * 0.01
            animal.peso_kg += delta
            logs.append({"dia": d+1, "peso_kg": round(animal.peso_kg, 3), "racion": round(racion,3)})
        return logs


# ================================================================================
# ARCHIVO 19/21: simulador_sensores.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/simulador_sensores.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 20/21: tareas_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/tareas_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 21/21: vacunacion_service.py
# Ruta: /home/pupi/Escritorio/DSistemas/DS-FINAL-CURSADO/TP-ShelterCare/TP-DS-ShelterCare/src/servicios/vacunacion_service.py
# ================================================================================

from typing import Dict, List
import datetime

class VacunaService:
    def __init__(self, persistencia=None):
        self._vacunas: Dict[int, List[dict]] = {}  # animal_id -> list of vacunas
        self.persistencia = persistencia
        self._load()

    def _load(self):
        if not self.persistencia:
            return
        data = self.persistencia.load('vacunas') or {}
        # data expected: {str(animal_id): [vacs]}
        self._vacunas = {int(k): v for k, v in data.items()}

    def _save(self):
        if not self.persistencia:
            return
        data = {str(k): v for k, v in self._vacunas.items()}
        self.persistencia.save('vacunas', data)

    def registrar_vacuna(self, animal_id: int, vacuna: str, lote: str, fecha: datetime.date, veterinario_id: int, proximo_refuerzo: datetime.date = None):
        entry = {"vacuna": vacuna, "lote": lote, "fecha": fecha.isoformat(), "veterinario_id": veterinario_id, "proximo_refuerzo": proximo_refuerzo.isoformat() if proximo_refuerzo else None}
        self._vacunas.setdefault(animal_id, []).append(entry)
        self._save()
        return entry

    def listar_vacunas(self, animal_id: int):
        return self._vacunas.get(animal_id, [])

    def animales_con_refuerzo_proximo(self, dias: int = 7):
        resultado = []
        hoy = datetime.date.today()
        for aid, vacs in self._vacunas.items():
            for v in vacs:
                if v.get('proximo_refuerzo'):
                    pr = datetime.date.fromisoformat(v['proximo_refuerzo'])
                    if 0 <= (pr - hoy).days <= dias:
                        resultado.append({"animal_id": aid, **v})
        return resultado

    def enviar_recordatorios(self, notificacion_service, dias:int=7):
        proximos = self.animales_con_refuerzo_proximo(dias=dias)
        for p in proximos:
            # notification placeholder: destino could be owner email in a richer model
            notificacion_service.enviar(destino="admin@refugio.local", asunto="Recordatorio vacuna", mensaje=f"Animal {p['animal_id']} tiene refuerzo próximo el {p['proximo_refuerzo']}")
        return len(proximos)


