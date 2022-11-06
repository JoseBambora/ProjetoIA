class Nodo:
    def __init__(self, coords, elem):
        self.coords = coords
        self.elem = elem


    def __str__(self):
        return self.elem.__str__()
