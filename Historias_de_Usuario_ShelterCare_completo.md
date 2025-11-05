# Historias de Usuario — Sistema de Gestión de Refugio de Animales

**Proyecto**: ShelterCare  
**Versión**: 1.0.0  
**Fecha**: Octubre 2025  
**Metodología**: User Story Mapping (Historias de Usuario detalladas)

---

## Índice

1. [Epic 1: Gestión del Refugio y Plantilla](#epic-1-gesti%C3%B3n-del-refugio-y-plantilla)
2. [Epic 2: Ingreso (Intake) de Animales](#epic-2-ingreso-intake-de-animales)
3. [Epic 3: Salud y Registro Médico](#epic-3-salud-y-registro-m%C3%A9dico)
4. [Epic 4: Cuidado, Alimentación y Estrategias de Alimentación](#epic-4-cuidado-alimentaci%C3%B3n-y-estrategias-de-alimentaci%C3%B3n)
5. [Epic 5: Adopciones y Seguimiento Post-Adopción](#epic-5-adopciones-y-seguimiento-post-adopci%C3%B3n)
6. [Epic 6: Voluntarios, Tareas y Planificación](#epic-6-voluntarios-tareas-y-planificaci%C3%B3n)
7. [Epic 7: Inventario y Suministros](#epic-7-inventario-y-suministros)
8. [Epic 8: Monitoreo en Tiempo Real y Alarmas (Observer)](#epic-8-monitoreo-en-tiempo-real-y-alarmas-observer)
9. [Epic 9: Persistencia, Reportes y Auditoría](#epic-9-persistencia-reportes-y-auditor%C3%ADa)
10. [Historias Técnicas (Patrones de Diseño: Singleton, Factory, Observer, Strategy)](#historias-t%C3%A9cnicas-patrones-de-dise%C3%B1o)

---

## Resumen del dominio

ShelterCare es un sistema para gestionar un refugio de animales pequeño o mediano. Cubre el registro e ingreso de animales, el control de su salud y vacunación, y las estrategias de alimentación y cuidado que varían según la especie y el estado del animal. También incluye la gestión de voluntarios y tareas, el control de inventario (alimentos, medicinas), procesos de adopción y monitoreo en tiempo real (temperatura, cámaras, sensores de movimiento y signos vitales cuando estén disponibles).

El sistema está pensado con fines educativos: demostrar la aplicación de patrones de diseño (Singleton, Factory, Observer, Strategy), la separación en capas (entidades / servicios / presentación) y buenas prácticas.

---

## Actores principales

- **Administrador del Refugio**: configura refugio, personal, políticas (vacunación, cuarentena), consulta reportes.  
- **Veterinario**: registra exámenes, recetas, vacunas, ordena procedimientos.  
- **Cuidador / Encargado de Turno**: realiza tareas diarias (alimentar, limpiar, medicar), registra observaciones.  
- **Voluntario**: realiza tareas asignadas, gestiona paseos / socialización.  
- **Cliente / Adoptante**: solicita adopciones, completa formularios y seguimiento post-adopción.  
- **Sistema de Monitoreo (automático)**: sensores y procesos que notifican eventos (Observer).  
- **Auditor / Inspector**: revisa trazabilidad, historiales y reportes.

---

## Epics y User Stories (completas)

> **Formato de cada historia**:  
> **Como** [actor]  
> **Quiero** [acción]  
> **Para** [beneficio]  
>
> **Criterios de Aceptación** (lista con checks)  
> **Detalles Técnicos**: clase(s) / servicio(s) / reglas.  
> **Ejemplo de uso** (fragmento de código de ejemplo cuando aplique).  
 **Trazabilidad**: `main.py` líneas ejemplo (referencia conceptual).


### Epic 1: Gestión del Refugio y Plantilla

#### US-001: Registrar Refugio / Sede
**Como** administrador del refugio  
**Quiero** registrar la sede del refugio con su nombre, dirección, capacidad y zonas (kennels, aislamiento, cuarentena, zona de adopción)  
**Para** tener datos oficiales y límites de ocupación por zona

**Criterios de Aceptación**
- [x] El sistema permite crear una sede con:
  - Nombre (texto, único)
  - Dirección (texto)
  - Capacidad total (entero > 0)
  - Zonas: lista con nombre, capacidad por zona (entero > 0)
- [x] No se puede crear una sede con capacidad <= 0 (lanza `ValueError`)
- [x] Se puede modificar dirección y capacidades (con validación)
- [x] El sistema muestra ocupación actual por zona

**Detalles Técnicos**
- Clase: `Sede` (`shelter/entidades/sede.py`)  
- Servicio: `SedeService` (`shelter/servicios/sede_service.py`)  
- Validaciones: `capacidad_total >= sum(capacidad_zonas)`; `nombre` único.

**Ejemplo**
```python
sede_service = SedeService()
sede = sede_service.crear_sede(
    nombre="Refugio Esperanza",
    direccion="Av. San Martín 123, Mendoza",
    capacidad_total=120,
    zonas=[{"nombre": "kennels", "capacidad": 80}, {"nombre":"cuarentena","capacidad":10}]
)
```

**Trazabilidad**: `main.py` líneas ~50-75

---

#### US-002: Registrar Personal y Roles
**Como** administrador  
**Quiero** registrar empleados y voluntarios con roles y certificaciones  
**Para** asignar tareas y validar permisos

**Criterios de Aceptación**
- [x] Cada persona tiene: ID único, nombre, rol (`Veterinario`, `Cuidador`, `Administrador`, `Voluntario`), contacto (email/teléfono), fecha de alta
- [x] Veterinarios requieren título/certificado (campo obligatorio)
- [x] Voluntarios pueden tener fecha de vencimiento de permisos
- [x] Se pueden desactivar perfiles (sin borrado físico)

**Detalles Técnicos**
- Clase: `Personal` y subclases `Veterinario`, `Cuidador`, `Voluntario` (`shelter/entidades/personal/`)  
- Servicio: `PersonalService` (`shelter/servicios/personal/personal_service.py`)  

**Ejemplo**
```python
personal_service.crear_personal(
    nombre="María López",
    rol="Veterinario",
    certificacion="Méd Vet Nº 12345",
    contacto={"email":"maria@ejemplo.org"}
)
```

---

### Epic 2: Ingreso (Intake) de Animales

#### US-003: Registrar Animal (Intake)
**Como** cuidador  
**Quiero** registrar un nuevo animal ingresado con sus datos básicos  
**Para** tener un expediente que permita su seguimiento

**Criterios de Aceptación**
- [x] Datos obligatorios: ID generado (único), especie (Dog, Cat, Bird, Rabbit, Other), nombre (opcional), edad estimada, sexo, fecha ingreso, estado (activo/rehabilitación/cuarentena), zona asignada
- [x] Validar que la zona tenga capacidad; si no la tiene, lanzar `CapacidadInsuficienteException`
- [x] Opcional: foto, observaciones iniciales
- [x] Si la especie es `Dog` o `Cat`, asignar tamaño (Small/Medium/Large) que impacta espacio/kennel

**Detalles Técnicos**
- Entidad: `Animal` y subclases `Perro`, `Gato`, `Ave`, `Conejo`, `Otro` (`shelter/entidades/animales/`)  
- Servicio: `AnimalFactory` (Factory Pattern) y `AnimalService` para lógica de negocio (`shelter/servicios/animales/`)

**Ejemplo**
```python
animal = animal_service.ingresar_animal(
    especie="Dog",
    nombre="Rex",
    edad_meses=12,
    sexo="M",
    zona="kennels"
)
```

---

#### US-004: Marcar Animal en Cuarentena
**Como** veterinario  
**Quiero** marcar un animal como en cuarentena con duración estimada y motivo  
**Para** evitar contacto y aplicar protocolos sanitarios

**Criterios de Aceptación**
- [x] Se registra fecha de inicio y fin estimado (fecha_fin > fecha_inicio)
- [x] Se registra motivo (enfermedad, observación, agresividad)
- [x] El animal no puede ser asignado a adopción mientras esté en cuarentena
- [x] Notificación a cuidadores asignados

**Detalles Técnicos**
- Clase: `Cuarentena` (o campos en `Animal`)  
- Servicio: `AnimalService.marcar_cuarentena(animal_id, fecha_fin, motivo)`

---

### Epic 3: Salud y Registro Médico

#### US-005: Registrar Examen Veterinario
**Como** veterinario  
**Quiero** registrar un examen con hallazgos, diagnóstico y prescripciones  
**Para** tener historial clínico completo del animal

**Criterios de Aceptación**
- [x] Registro contiene: fecha, veterinario, signos observados, diagnóstico, tratamiento, medicamentos recetados, próximas citas
- [x] Genera entrada en el historial médico del animal
- [x] Permite adjuntar archivos (imágenes, radiografías) opcionales
- [x] Si el tratamiento incluye medicamento, el inventario se decrementa (si existe stock); si no hay stock lanza `InventarioInsuficienteException`

**Detalles Técnicos**
- Entidad: `HistoriaMedica`, `Examen` (`shelter/entidades/medicina/`)  
- Servicio: `MedicinaService` (`shelter/servicios/medicina/`)  
- Integración: `InventarioService`

**Ejemplo**
```python
medicina_service.registrar_examen(
    animal_id=1,
    vet_id=3,
    hallazgos="Lesión en pata trasera",
    diagnostico="Fractura probable",
    prescripcion=[{"medicamento":"Antibiótico X", "dosis":"10mg/12h", "dias":7}]
)
```

---

#### US-006: Control de Vacunación y Recordatorio
**Como** administrador / veterinario  
**Quiero** registrar vacunas aplicadas y programar recordatorios para próximas vacunas  
**Para** mantener la trazabilidad y no olvidar refuerzos

**Criterios de Aceptación**
- [x] Se registra vacuna, lote, fecha, veterinario y próxima fecha de refuerzo (si aplica)  
- [x] Sistema genera lista de animales con vacunación próxima en X días  
- [x] Se envían notificaciones (email/alerta interna) a responsables

**Detalles Técnicos**
- Entidad: `Vacuna` vinculada a `HistoriaMedica`  
- Servicio: `VacunaService`, `NotificacionService`  
- Observer: `NotificacionService` puede estar suscrito a eventos de programación (ver epic Observer)

---

#### US-007: Simular evolución de salud y peso del animal
**Como** investigador veterinario  
**Quiero** poder simular la evolución del estado de salud y peso de un animal a lo largo de días/semanas  
**Para** validar políticas de alimentación y observar efectos de tratamientos en el tiempo

**Criterios de Aceptación**
- [x] Hay una función/scheduler de simulación que avanza N días y aplica reglas: cambio de peso según ración recibida, efecto de tratamientos, y estado de rehabilitación
- [x] La simulación permite parametrizar: días a simular, frecuencia de alimentación, condiciones iniciales (peso, diagnóstico)
- [x] Se generan logs resumidos por animal con métricas por día (peso, estado, medicamentos administrados)

**Detalles Técnicos**
- Servicio: `SimuladorSaludService` (`shelter/servicios/simulador/salud_simulator.py`)  
- Reglas: incrementar/decrementar `peso_kg` según `racion_consumida / racion_recomendada`; aplicar efectos temporales de tratamientos (ej. esteroides aumentan apetito)  
- Uso: utilizable por `main.py` para demostraciones y por responsables para ajustar estrategias de alimentación

**Ejemplo**
```python
sim = SimuladorSaludService()
sim.simular(animal_id=1, dias=30, frecuencia_alimentacion=2)
```

**Trazabilidad**: `main.py` demo (ver historia de demo end-to-end)


### Epic 4: Cuidado, Alimentación y Estrategias de Alimentación

#### US-008: Definir Estrategias de Alimentación por Especie (Strategy)
**Como** encargado de nutrición  
**Quiero** definir estrategias de alimentación intercambiables por especie/condición  
**Para** aplicar planes nutricionales distintos sin cambiar lógica central

**Criterios de Aceptación**
- [x] Implementar al menos dos estrategias: `AlimentacionEstandarStrategy` y `AlimentacionMedicaStrategy`  
- [x] Cada animal tiene una estrategia asignada (puede cambiarse)  
- [x] Servicio `AlimentacionService` delega el cálculo de raciones a la estrategia  
- [x] Cambiar estrategia no requiere refactor en `AlimentacionService`

**Detalles Técnicos**
- Interfaz: `AlimentacionStrategy` con método `calcular_racion(animal, fecha, condicion)`  
- Implementaciones: `PorPesoStrategy`, `PorEdadStrategy`, `MedicaStrategy`  
- Servicio: `AlimentacionService` (usa Strategy Pattern)

**Ejemplo**
```python
alimentacion_service.set_strategy(animal_id=1, strategy=PorPesoStrategy())
racion = alimentacion_service.calcular_racion(animal_id=1)
```

---

#### US-009: Registrar Alimentación Diaria
**Como** cuidador  
**Quiero** registrar cada acto de alimentación (quién, cuándo, qué cantidad)  
**Para** verificar cumplimiento y ajustar raciones

**Criterios de Aceptación**
- [x] Registro incluye fecha/hora, personal, alimento, peso entregado, observaciones  
- [x] Historial accesible por animal y por día  
- [x] Si la cantidad entregada difiere > X% de la ración recomendada, generar alerta para revisión

**Detalles Técnicos**
- Entidad: `RegistroAlimentacion`  
- Servicio: `AlimentacionService.registrar_alimentacion(...)`

---

### Epic 5: Adopciones y Seguimiento Post-Adopción

#### US-010: Proceso de Solicitud de Adopción
**Como** cliente/adoptante  
**Quiero** presentar una solicitud de adopción con formulario y referencias  
**Para** iniciar la evaluación del perfil para adoptar un animal

**Criterios de Aceptación**
- [x] Formulario incluye datos personales, domicilio, referencias, experiencia con animales  
- [x] Sistema valida campos obligatorios (nombre, documento, domicilio, teléfono/email)  
- [x] Solicitud queda en estado `pendiente` hasta revisión por trabajador  
- [x] Permite adjuntar documentos (comprobantes de domicilio, autorización de vivienda si corresponde)

**Detalles Técnicos**
- Entidad: `SolicitudAdopcion`  
- Servicio: `AdopcionService` (`shelter/servicios/adopcion/adopcion_service.py`)

---

#### US-011: Evaluar y Aceptar/Rechazar Solicitud de Adopción
**Como** trabajador responsable  
**Quiero** evaluar solicitudes, programar visita domiciliaria y aprobar o rechazar  
**Para** asegurar una buena colocación y reducir retornos

**Criterios de Aceptación**
- [x] Se puede cambiar estado: `pendiente` → `aprobada`/`rechazada`/`en_revision`  
- [x] Al aprobar, crea un contrato de adopción y registra fecha de entrega  
- [x] En caso de rechazo se genera motivo y se notifica al solicitante

**Detalles Técnicos**
- Servicio: `AdopcionService.evaluar_solicitud(...)`  
- Genera `ContratoAdopcion` (objeto con clausulas y firmas digitales/placeholder)

---

#### US-012: Seguimiento Post-Adopción
**Como** trabajador del refugio  
**Quiero** realizar seguimientos (contacto a X días, visita) y registrar estado del animal  
**Para** monitorear adaptación y reducir devoluciones

**Criterios de Aceptación**
- [x] Programar seguimientos automáticos (ej. 7, 30, 90 días)  
- [x] Registro de resultado de seguimiento (satisfactorio/observaciones)  
- [x] Si hay reporte de problema, abrir caso de retorno o asesoría

**Detalles Técnicos**
- Servicio: `PostAdopcionService`  
- Notificaciones automáticas: `NotificacionService`


#### US-013: Seguimiento post-adopción con reglas temporales estrictas
**Como** trabajador del refugio  
**Quiero** que los seguimientos post-adopción se programen y ejecuten automáticamente con reglas temporales (7/30/90 días) y escalamiento en caso de no respuesta  
**Para** asegurar que las adopciones se monitorean y dar soporte temprano si hay problemas

**Criterios de Aceptación**
- [x] Se programan automáticamente seguimientos en 7, 30 y 90 días al completar una adopción  
- [x] Si no se recibe respuesta en X días, el caso se escala a un trabajador y se marca para visita domiciliaria  
- [x] Registro de resultado del seguimiento y posibilidad de abrir caso de retorno o asesoría

**Detalles Técnicos**
- Servicio: `PostAdopcionService` — añadir `programar_seguimientos(adopcion_id)` y `evaluar_respuesta(adopcion_id)`  
- Uso: integrado con el scheduler/simulador de tareas y `ReportesService` para ver tasas de cumplimiento


### Epic 6: Voluntarios, Tareas y Planificación

#### US-014: Crear y Asignar Tareas Diarias
**Como** coordinador de voluntarios  
**Quiero** crear tareas (limpieza, paseos, socialización) y asignarlas a personal/voluntarios  
**Para** organizar el trabajo diario

**Criterios de Aceptación**
- [x] Tarea tiene: ID, descripción, prioridad, duración estimada, asignado(s), fecha/hora programada, estado  
- [x] Se puede reasignar y marcar como completada  
- [x] Reglas: un voluntario no puede tener > N tareas simultáneas (configurable)

**Detalles Técnicos**
- Entidad: `Tarea`  
- Servicio: `TareasService`  
- Integración: `CalendarioService` / exportación iCal opcional

---

#### US-015: Registro de Asistencia y Horas de Voluntariado
**Como** voluntario  
**Quiero** fichar entrada/salida y registrar horas  
**Para** contabilizar horas y validar requisitos de servicio comunitario

**Criterios de Aceptación**
- [x] Registro de inicio y fin de turno por voluntario  
- [x] Cálculo de horas totales por periodo (semana/mes)  
- [x] Permite exportar informe de horas

---

### Epic 7: Inventario y Suministros

#### US-016: Control de Inventario (Alimentos y Medicamentos)
**Como** administrador  
**Quiero** controlar stock de alimentos y medicación para evitar faltantes  
**Para** garantizar suministros y planificar compras

**Criterios de Aceptación**
- [x] Producto con: SKU, nombre, categoría, cantidad actual, unidad, punto de reorden  
- [x] Registrar entradas y salidas (por compra o consumo)  
- [x] Cuando stock < punto de reorden, generar alerta de compra  
- [x] Integración con `MedicinaService` para decrementar stock al prescribir

**Detalles Técnicos**
- Entidad: `ProductoInventario`  
- Servicio: `InventarioService`

---

#### US-017: Generar Órdenes de Compra
**Como** administrador  
**Quiero** generar órdenes de compra automáticas cuando el stock esté bajo  
**Para** automatizar reabastecimiento

**Criterios de Aceptación**
- [x] Orden de compra contiene items, cantidades sugeridas, proveedor (opcional)  
- [x] Se puede exportar a PDF/CSV (placeholder)  
- [x] Cambios de estado: `pendiente` → `ordenada` → `recibida` y actualiza inventario


#### US-018: Manejo de concurrencia en Inventario
**Como** administrador  
**Quiero** que el sistema maneje acceso concurrente al inventario (prescripciones y recepciones simultáneas)  
**Para** evitar inconsistencias y stock negativo cuando múltiples actores operen sobre el mismo ítem

**Criterios de Aceptación**
- [x] Las operaciones de decremento/incremento de stock son atómicas desde la perspectiva del `InventarioService`  
- [x] Se documenta la política de locks/serialización a usar (lock por SKU o mecanismo equivalente)  
- [x] Casos de conflicto (dos prescripciones que consumen el último lote) resultan en una de las transacciones recibiendo `InventarioInsuficienteException` y la otra completándose correctamente

**Detalles Técnicos**
- Servicio: `InventarioService` — implementar locking por SKU y checks previos a la confirmación de operación  
- Uso: integrado con `MedicinaService` (prescripciones) y con procesos de recepción de órdenes

**Ejemplo**
```python
inventario.decrementar_stock(sku="MED-X", cantidad=2)
```


### Epic 8: Monitoreo en Tiempo Real y Alarmas (Observer)

#### US-019: Integrar Sensores de Temperatura/Humedad/Luz
**Como** encargado técnico  
**Quiero** que sensores envíen lecturas periódicas y notifiquen observadores  
**Para** mantener condiciones ambientales adecuadas y actuar automáticamente

**Criterios de Aceptación**
- [x] Sensores ejecutan lecturas periódicas (configurable) y notificarán a observadores (Observer Pattern)  
- [x] Observadores posibles: `ControlClimaService`, `NotificacionService`, `RegistroEventosService`  
- [x] Lecturas fuera de rango generan eventos de alerta

**Detalles Técnicos**
- Implementar `Observable[float]` / `Observer[float]` como en el ejemplo forestal  
- Sensores: `SensorTemperaturaTask`, `SensorHumedadTask`, `SensorMovimientoTask`

---

#### US-020: Alarmas y Acciones Automáticas
**Como** sistema de control  
**Quiero** activar alarmas o acciones (p. ej. encender calefacción, enviar alerta) cuando se detecte una condición crítica  
**Para** reducir riesgos para animales

**Criterios de Aceptación**
- [x] Condiciones configurables: temp < X, humedad > Y, movimiento en zona restringida  
- [x] Acciones configurables: enviar email/SMS, notificación interna, activar actuador (placeholder)  
- [x] Se guarda log de acción y quién la autorizó/ejecutó

**Detalles Técnicos**
- Servicio: `ControlClimaService`, `AlarmaService`  
- Observer suscrito a sensores; usa `ActionHandler` para ejecutar acciones


#### US-021: Simulación masiva de sensores y picos de eventos
**Como** encargado técnico  
**Quiero** poder configurar y simular N sensores y picos de eventos masivos  
**Para** verificar la robustez del sistema de observadores, colas de eventos y manejo de alarmas bajo carga

**Criterios de Aceptación**
- [x] Se puede definir cantidad N de sensores y la frecuencia de lecturas para la simulación  
- [x] La simulación permite provocar picos (burst) de lecturas fuera de rango y validar que `NotificacionService` y `RegistroEventosService` reciben los eventos esperados
- [x] Se generan métricas de la simulación: total eventos, eventos críticos, latencia de notificación (estimada)

**Detalles Técnicos**
- Servicio: `SimuladorSensoresService` (`shelter/servicios/simulador/sensores_simulator.py`)  
- Uso: utilizable por `main.py` para demostraciones y validación de Observer bajo carga

**Ejemplo**
```python
sim_sens = SimuladorSensoresService()
sim_sens.simular(cantidad_sensores=50, duracion_seg=60, probabilidad_pico=0.05)
```


### Epic 9: Persistencia, Reportes y Auditoría

#### US-022: Persistir Datos y Recuperación
**Como** auditor  
**Quiero** que los datos principales (animales, historia médica, adopciones, inventario) se persistan y se puedan recuperar  
**Para** garantizar trazabilidad y recuperación ante fallos

**Criterios de Aceptación**
- [x] Soporta persistencia en disco (pickle/JSON/DB sencillo) — en la versión educativa, uso de serialización local está OK  
- [x] Export/import de registros por entidad (por ejemplo `registro_{animal_id}.json`)  
- [x] Validaciones de integridad al recuperar (hash/simple checksum)

**Detalles Técnicos**
- Servicio: `PersistenciaService` con adaptadores (JSON, Pickle)  
- Configurable: `data/` por defecto


#### US-023: Persistencia: manejo de errores y rollback básico
**Como** auditor  
**Quiero** que las operaciones de persistencia tengan manejo de errores y, cuando sea apropiado, rollback básico para mantener la consistencia de datos en disco  
**Para** evitar dejar datos parciales o inconsistentes ante fallos durante series de operaciones

**Criterios de Aceptación**
- [x] `PersistenciaService` documenta y aplica una política mínima de atomicidad para operaciones compuestas (por ejemplo: escribir archivo temporal y renombrar al finalizar)  
- [x] En caso de error durante un conjunto de operaciones relacionadas, el servicio restaura el estado previo conocido cuando sea posible o marca el índice como inconsistente para revisión manual
- [x] Se registra el error y se genera un aviso en los logs para auditoría

**Detalles Técnicos**
- Servicio: `PersistenciaService` — implementar write-to-temp + rename, y mantener backups simples (`.bak`) para permitir restauración manual


#### US-024: Reportes (ocupación, vacunas, adopciones)
**Como** administrador  
**Quiero** generar reportes para indicadores claves: ocupación por zona, animales vacunados en periodo, adopciones por mes  
**Para** toma de decisiones y presentación a autoridades

**Criterios de Aceptación**
- [x] Reporte de ocupación actual (por zona y total)  
- [x] Reporte de vacunas realizadas en X periodo  
- [x] Reporte de adopciones por periodo con detalle de especie y edad

**Detalles Técnicos**
- Servicio: `ReportesService` — export CSV/JSON (implementación básica)

---

### Historias Técnicas (Patrones de Diseño)

> Estas historias son indispensables y deberán mapearse a criterios de aceptación en la rúbrica técnica.

#### US-025: Implementar Singleton para el Registro Central de Servicios
**Como** arquitecto del sistema  
**Quiero** un `ShelterServiceRegistry` que sea Singleton y thread-safe  
**Para** centralizar acceso a servicios (AnimalService, InventarioService, etc.)

**Criterios de Aceptación**
- [x] Singleton con `__new__` y lock (double-checked)  
- [x] `get_instance()` disponible  
- [x] Registro de handlers para dispatch polimórfico (ej. mostrar datos según especie)

**Detalles Técnicos**
- Clase: `ShelterServiceRegistry` (`shelter/servicios/registry.py`)  
- Uso: `registry = ShelterServiceRegistry.get_instance()`

---

#### US-026: Implementar Factory para creación de animales
**Como** desarrollador  
**Quiero** una `AnimalFactory` que cree instancias de `Perro`, `Gato`, `Ave`, `Conejo`, `Otro` según parámetro  
**Para** evitar instanciación directa y facilitar extensibilidad

**Criterios de Aceptación**
- [x] Método estático `crear_animal(especie:str, **kwargs)`  
- [x] Diccionario de factories (no cascada if/elif)  
- [x] Valida especie desconocida → `ValueError`

**Detalles Técnicos**
- Archivo: `shelter/patrones/factory/animal_factory.py`

---

#### US-027: Implementar Observer para sensores y notificaciones
**Como** encargado técnico  
**Quiero** una implementación genérica `Observable[T]` y `Observer[T]`  
**Para** desacoplar sensores y consumidores

**Criterios de Aceptación**
- [x] Generic `Observable[T]` con `agregar_observador()` y `notificar_observadores(evento)`  
- [x] Observers se registran y responden a eventos (ControlClima, RegistroEventos, Notificaciones)  
- [x] Sensores ejecutan en threads daemon y hacen `notificar_observadores`

**Detalles Técnicos**
- Ruta: `shelter/patrones/observer/`

---

#### US-028: Implementar Strategy para alimentación y cuidado
**Como** nutricionista del refugio  
**Quiero** implementar `AlimentacionStrategy` que permita intercambiar políticas de cálculo de ración y frecuencia de alimentación  
**Para** soportar dietas estándar y especiales fácilmente

**Criterios de Aceptación**
- [x] Interfaz abstracta `AlimentacionStrategy`  
- [x] Mínimo 2 implementaciones concretas (`PorPesoStrategy`, `CondicionMedicaStrategy`)  
- [x] Inyección de la strategy en `AlimentacionService` vía constructor

**Detalles Técnicos**
- Ruta: `shelter/patrones/strategy/`

---

## Historias técnicas y mapeo a clases / servicios / módulos

Resumen de módulos propuestos (estructura de proyecto sugerida):

```
sheltercare/
├── src/
│   ├── entidades/
│   │   ├── animales/
│   │   │   ├── __init__.py
│   │   │   ├── animal.py
│   │   │   ├── perro.py
│   │   │   ├── gato.py
│   │   │   └── ...
│   │   ├── personal/
│   │   ├── medicina/
│   │   └── inventario/
│   ├── servicios/
│   │   ├── animales/
│   │   ├── personal/
│   │   ├── medicina/
│   │   ├── inventario/
│   │   ├── adopcion/
│   │   ├── sede/
│   │   └── registry.py  # Singleton
│   ├── patrones/
│   │   ├── factory/
│   │   ├── observer/
│   │   └── strategy/
│   ├── riego/ (opcional -> control_clima)
│   ├── persistence/
│   └── main.py
└── data/
```

Clases/Servicios claves (mapeo rápido):
- `Animal` (+subclases) — `AnimalService`  
- `AnimalFactory` — crea animales  
- `ShelterServiceRegistry` — singleton que devuelve servicios  
- `AlimentacionStrategy` (+implementaciones) — usado por `AlimentacionService`  
- `Observable/Observer` — sensores y notificaciones  
- `InventarioService` — control stock  
- `MedicinaService` — exámenes/vacunas  
- `AdopcionService` — gestión de solicitudes y contratos  
- `TareasService` — planificador de tareas

---

## Constantes y validaciones importantes

Ejemplo de constantes que centralizar en `constantes.py`:

```python
# capacidades
CAPACIDAD_MINIMA = 1

# tiempos
TIEMPO_SEGUIMIENTO_POST_ADOPCION_DIAS = [7, 30, 90]

# alimentacion
RACION_POR_KG_PERRO = 0.03  # 3% del peso corporal (ejemplo)
RACION_POR_KG_GATO = 0.025

# sensores
TEMP_MIN_OK = 15.0  # grados C
TEMP_MAX_OK = 28.0
HUMEDAD_MIN_OK = 30.0
HUMEDAD_MAX_OK = 70.0

# inventario
PUNTO_REORDEN_DEFAULT = 10
```

Validaciones comunes:
- Capacidades y cantidades > 0  
- Fechas coherentes (fecha_fin > fecha_inicio)  
- No permitir adopción si animal en cuarentena o sin vacunas obligatorias (según política)  
- Control de concurrencia en Singleton y servicios que manipulan inventario

---

## Ejemplos de uso / snippets

**Factory — crear animal**
```python
from shelter.patrones.factory.animal_factory import AnimalFactory

animal = AnimalFactory.crear_animal("Dog", nombre="Rex", edad_meses=12, sexo="M", tamano="Medium")
```

**Singleton — registry básico**
```python
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
```

**Observer — sensor simple**
```python
class Observable(Generic[T]):
    def __init__(self):
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, o: Observer[T]) -> None:
        self._observadores.append(o)

    def notificar_observadores(self, evento: T) -> None:
        for o in list(self._observadores):
            o.actualizar(evento)
```

**Strategy — alimentación**
```python
class AlimentacionStrategy(ABC):
    @abstractmethod
    def calcular_racion(self, animal: "Animal", fecha: date) -> float:
        """Calcula la ración recomendada para el animal en la fecha dada.
        Implementaciones concretas deben sobrescribir este método.
        """
        raise NotImplementedError()

class PorPesoStrategy(AlimentacionStrategy):
    def calcular_racion(self, animal, fecha):
        if isinstance(animal, Perro):
            return animal.peso_kg * RACION_POR_KG_PERRO
        if isinstance(animal, Gato):
            return animal.peso_kg * RACION_POR_KG_GATO
        return 0.1
```

        **Trazabilidad**: `main.py` líneas ejemplo (referencia conceptual).
## Trazabilidad y notas para implementación

- Diseñar `main.py` de demostración que recorra un flujo típico: crear sede → registrar personal → ingresar animales → registrar examen → asignar alimentación → simular sensores. (Útil para checks dinámicos en la rúbrica).  
- Añadir ejemplos en README y pruebas unitarias para cada patrón (tests que verifiquen que Singleton devuelve misma instancia, Factory lanza error en especie desconocida, Observer notifica, Strategy produce raciones diferentes).  
- Para la entrega académica, preferir persistencia simple (JSON/Pickle) y documentación clara en README; si hay tiempo, agregar capa de abstracción para DB.

---

## Observaciones finales

He diseñado las historias de usuario para cubrir **funcionalidad equivalente y escala** del proyecto de referencia (gestión forestal), pero adaptadas al dominio de un refugio de animales. Las historias incluyen criterios de aceptación claros, detalles técnicos, entidades y servicios sugeridos, y mapeo a los cuatro patrones solicitados (Singleton, Factory, Observer, Strategy).