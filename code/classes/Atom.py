class Atom:
    """ This class holds atom objects. """ 

    def __init__(self, label, coordinates):
        self.label = label
        
        # TODO: this only works for elements with an atomic lable of 1 letter
        self.symbol = label[:1]

        self.distance_to_center = None
        self.in_central_group = False

        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

    def add_to_central_group(self):
        self.in_central_group = True

    def set_color(self, color):
        self.color = color

    def add_fragment_id(self, fragment_id):
        self.fragment_id = fragment_id

    def set_vdw_radius(self, radius):
        self.vdw_radius = radius

    def __str__(self):
        return self.label + ": " + str(self.x) + ", " + str(self.y) + ", " + str(self.z)

