# TP-DS-ShelterCare
## Alumno: Juan Alejo Patiño
## Legajo: 61160

# ShelterCare — Demo Educativa

Resumen rápido
--------------
ShelterCare es un proyecto educativo que simula la gestión de un refugio de animales. Implementa patrones de diseño (Singleton, Factory, Observer, Strategy), persistencia simple en JSON y varios servicios que modelan operaciones reales de un refugio: ingreso de animales, atención médica, alimentación, cuarentenas, adopciones, inventario y notificaciones.

Qué hay en este repositorio
----------------------------
- `src/` — código fuente principal.
  - `entidades/` — modelos de dominio (Animal, Perro, Gato, Sede, Personal, etc.).
  - `servicios/` — capas de negocio (AnimalService, InventarioService, VacunaService, AdopcionService, QuarantineService, etc.).
  - `patrones/` — implementaciones de patrones (factory, observer, strategy).
- `main.py` — script demo que arma los servicios, corre un flujo de ejemplo y persiste datos en `data/`.
- `data/` — carpeta donde la aplicación persiste JSON (creada en tiempo de ejecución).

Características implementadas
----------------------------
- Creación y persistencia de sedes, personal y animales.
- Factory para crear animales (`src/patrones/factory/animal_factory.py`).
- Registro central de servicios como Singleton (`src/servicios/registry.py`).
- Observer: simulador de sensores y servicio de alarmas (`src/patrones/observer`, `src/servicios/simulador_sensores.py`, `src/servicios/alarma_service.py`).
- Strategy para cálculo de ración de alimento (`src/patrones/strategy/alimentacion.py` + `alimentacion_service`).
- Flujo de atención médica con decremento de inventario (prescripciones).
- Gestión de cuarentenas y bloqueo de aprobaciones de adopción mientras el animal está en cuarentena.
- Persistencia JSON segura (escribe a un archivo temporal y renombra) en `src/servicios/persistencia_service.py`.
- Demo con salida por consola formateada (secciones numeradas y JSON pretty-print).

Cómo ejecutar la demo
---------------------
Requisitos: Python 3.x.

Desde la raíz del proyecto (donde está `main.py`) ejecuta:

```bash
python3 main.py
```

Qué esperar al correr la demo
-----------------------------
- El script crea una sede demo, añade personal, ingresa un animal, calcula raciones, registra un examen médico y simula sensores y salud.
- Los datos se guardan en `data/` (por ejemplo `animales.json`, `inventario.json`, `adopciones.json`, `cuarentenas.json`).
- La salida en consola está organizada por secciones y contiene JSON formateado para facilitar la lectura.