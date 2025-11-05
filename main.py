import sys
import json
import traceback
from pathlib import Path

# ensure project src is on sys.path
ROOT = Path(__file__).parent
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.servicios.persistencia_service import PersistenciaService
from src.servicios.sede_service import SedeService
from src.servicios.personal_service import PersonalService
from src.servicios.animal_service import AnimalService
from src.servicios.medicina_service import MedicinaService
from src.servicios.inventario_service import InventarioService
from src.servicios.alimentacion_service import AlimentacionService
from src.servicios.simulador_salud import SimuladorSaludService
from src.servicios.simulador_sensores import SimuladorSensoresService
from src.servicios.registry import ShelterServiceRegistry
from src.entidades.inventario import ProductoInventario
from src.patrones.strategy.alimentacion import PorPesoStrategy
from src.servicios.vacunacion_service import VacunaService
from src.servicios.postadopcion_service import PostAdopcionService
from src.servicios.tareas_service import TareasService
from src.servicios.registro_alimentacion_service import RegistroAlimentacionService
from src.servicios.alarma_service import AlarmaService
from src.servicios.adopcion_service import AdopcionService


def demo():
    print("==============================================")
    print("SHELTERCARE - DEMO EDUCATIVA")
    print("==============================================\n")
    try:
        persist = PersistenciaService(data_dir=str(ROOT / "data"))

        # services
        sede_svc = SedeService()
        personal_svc = PersonalService()
        inventario_svc = InventarioService()
        # attach persistence for inventory and load existing
        inventario_svc.persistencia = persist
        inventario_svc.load_all()
        alimentacion_svc = AlimentacionService()
        registro_alim_svc = None
        medicina_svc = MedicinaService(inventario=inventario_svc)
        animal_svc = AnimalService(persistencia=persist)
        # additional services (with persistence where applicable)
        vacunas_svc = VacunaService(persistencia=persist)
        postadop_svc = PostAdopcionService(persistencia=persist)
        adopcion_svc = AdopcionService(persistencia=persist)
        tareas_svc = TareasService(persistencia=persist)
        registro_alim_svc = RegistroAlimentacionService(persistencia=persist)
        # quarantine service
        from src.servicios.quarantine_service import QuarantineService
        quarantine_svc = QuarantineService(persistencia=persist)
        # notification & orders
        from src.servicios.notificacion_service import NotificacionService
        from src.servicios.orden_compra_service import OrdenCompraService
        notificacion_svc = NotificacionService()
        orden_svc = OrdenCompraService(persistencia=persist)
        # attach persistence to personal
        personal_svc.persistencia = persist

        # registry
        reg = ShelterServiceRegistry.get_instance()
        reg.register('sede', sede_svc)
        reg.register('personal', personal_svc)
        reg.register('inventario', inventario_svc)
        reg.register('alimentacion', alimentacion_svc)
        reg.register('medicina', medicina_svc)
        reg.register('animales', animal_svc)
        reg.register('vacunas', vacunas_svc)
        reg.register('adopcion', adopcion_svc)
        reg.register('postadopcion', postadop_svc)
        reg.register('cuarentenas', quarantine_svc)
        reg.register('tareas', tareas_svc)
        reg.register('alimentaciones', registro_alim_svc)
        reg.register('notificacion', notificacion_svc)
        reg.register('ordenes', orden_svc)
        # asistencia (fichajes)
        from src.servicios.asistencia_service import AsistenciaService
        asistencia_svc = AsistenciaService(persistencia=persist)
        reg.register('asistencia', asistencia_svc)
        # attach cross-service wiring
        # wire postadop into adopcion service
        try:
            adopcion_svc.attach_postadop_service(postadop_svc)
        except Exception:
            pass
        # attach quarantine to animal service and adopcion
        try:
            animal_svc.attach_quarantine_service(quarantine_svc)
            adopcion_svc.attach_postadop_service(postadop_svc)
        except Exception:
            pass

        # 1. crear sede
        print("1. CREAR SEDE")
        sede = sede_svc.crear_sede(nombre="Refugio Demo", direccion="Calle Falsa 123", capacidad_total=50, zonas=[{"nombre":"kennels","capacidad":30},{"nombre":"cuarentena","capacidad":5}])
        print(json.dumps(sede.to_dict(), ensure_ascii=False, indent=2))

        # 2. crear personal
        print("\n2. CREAR PERSONAL")
        p = personal_svc.crear_personal(nombre="Dr. Ana", rol="Veterinario", contacto={"email":"ana@refugio.org"})
        print(json.dumps(p.to_dict(), ensure_ascii=False, indent=2))

        # 3. inventario
        print("\n3. INVENTARIO: añadir ítems iniciales")
        prod = ProductoInventario(sku="MED-X", nombre="Antibiótico X", categoria="Medicamento", cantidad=10, unidad="botes")
        inventario_svc.add_item(prod)
        print(json.dumps([i.to_dict() for i in inventario_svc.list_items()], ensure_ascii=False, indent=2))

        # 4. ingresar animal
        print("\n4. INGRESAR ANIMAL")
        a = animal_svc.ingresar_animal(especie="Dog", nombre="Rex", edad_meses=12, sexo='M', zona='kennels', peso_kg=12.5)
        print(json.dumps(a.to_dict(), ensure_ascii=False, indent=2))

        # asignar strategy
        alimentacion_svc.set_strategy(a.id, PorPesoStrategy())
        # attach registro de alimentacion
        alimentacion_svc.attach_registro_service(registro_alim_svc)
        racion = alimentacion_svc.calcular_racion(a)
        print(f"Ración calculada para {a.nombre}: {racion:.3f} kg")

        # registrar examen
        # 5. atención médica
        print("\n5. ATENCIÓN MÉDICA: registrar examen y aplicar prescripción")
        examen = medicina_svc.registrar_examen(animal_id=a.id, vet_id=p.id, hallazgos="Cojera leve", diagnostico="Esguince", prescripcion=[{"medicamento":"MED-X","cantidad":1}])
        print("Examen registrado:", json.dumps({"diagnostico": examen.diagnostico}, ensure_ascii=False))
        print("Inventario después de prescripción:")
        print(json.dumps([i.to_dict() for i in inventario_svc.list_items()], ensure_ascii=False, indent=2))

        # simular salud
        sim = SimuladorSaludService(animal_service=animal_svc, alimentacion_service=alimentacion_svc)
        logs = sim.simular(animal_id=a.id, dias=7, frecuencia_alimentacion=2)
        print("\n6. SIMULACIÓN DE SALUD (7 días):")
        for l in logs:
            print(json.dumps(l, ensure_ascii=False))

        # simular sensores (rápido)
        # attach alarma observer
        sim_sens = SimuladorSensoresService()
        alarma = AlarmaService()
        sim_sens.observable.agregar_observador(alarma)
        events = sim_sens.simular(cantidad_sensores=5, duracion_seg=2, probabilidad_pico=0.2)
        print(f"\n7. EVENTOS DE SENSORES: {len(events)} eventos generados")

        # persistir animales
        animal_svc.persist_all()
        print("\nAnimales persistidos en data/animales.json")
        # persist other entities
        vacunas_svc._save()
        postadop_svc._save()
        tareas_svc._save()
        registro_alim_svc._save()
        # check reorders and create simple order if needed
        sugerencias = inventario_svc.check_reorden()
        if sugerencias:
            orden = orden_svc.crear_orden(sugerencias)
            print("Orden de compra creada:")
            print(json.dumps(orden, ensure_ascii=False, indent=2))
        # enviar recordatorios de vacunas (ejemplo)
        try:
            enviados = vacunas_svc.enviar_recordatorios(notificacion_svc, dias=30)
            print(f"Recordatorios de vacunas enviados: {enviados}")
        except Exception:
            pass
        # housekeeping: evaluar seguimientos post-adopcion y notificar escalados
        try:
            escalados = postadop_svc.evaluar_respuestas_y_escalar(dias_sin_respuesta=7)
            if escalados:
                for e in escalados:
                    notificacion_svc.enviar(destino="coordinador@refugio.local", asunto="Seguimiento escalado", mensaje=f"Adopcion {e['adopcion_id']} con seguimiento {e['fecha']}")
                print(f"Seguimientos escalados: {len(escalados)}")
        except Exception:
            pass

        # demo completed banner
        print("\n==============================================")
        print("DEMO COMPLETADO")
        print("==============================================")
    except Exception as e:
        print("\nERROR EN LA EJECUCIÓN DEL DEMO:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        traceback.print_exc()


if __name__ == '__main__':
    demo()
