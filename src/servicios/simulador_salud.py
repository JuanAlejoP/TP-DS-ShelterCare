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
