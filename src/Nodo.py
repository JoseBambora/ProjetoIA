class Nodo:
    def __init__(self, coords, elem):
        self.coords = coords
        self.elem = elem
        self.heuristica = 0

    def __str__(self):
        return self.elem.__str__() + " " + str(self.heuristica)
