from inventory import Inventory
class Spacecraft(object):
    def __init__(self, name, nation, payload_mass, payload_volume, mass,
                base_costs, fuel_to_weight):

        self.name = name
        self.nation = nation
        self.payload_mass = payload_mass
        self.payload_volume = payload_volume
        self.mass = mass
        self.base_costs = base_costs
        self.fuel_to_weight = fuel_to_weight
        self.mass_per_volume = payload_mass / payload_volume
        self.inventory = Inventory()
    def __str__(self):
        return str(self.name) + ' ' + str(self.payload_mass) + ' ' + \
        str(self.payload_volume) + ' ' + str(self.mass) + ' ' +\
        str(self.base_costs) + ' ' + str(self.fuel_to_weight)
    def take(self, item):
        self.inventory.add(item)
