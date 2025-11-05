from .animal import Animal

class Perro(Animal):
    especie = "Dog"

    def __init__(self, *args, **kwargs):
        super().__init__(especie=self.especie, *args, **kwargs)
