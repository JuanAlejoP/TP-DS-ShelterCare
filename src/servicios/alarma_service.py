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
