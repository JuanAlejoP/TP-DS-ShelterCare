from .animal import Animal

class Gato(Animal):
    especie = "Cat"

    def __init__(self, *args, **kwargs):
        super().__init__(especie=self.especie, *args, **kwargs)
