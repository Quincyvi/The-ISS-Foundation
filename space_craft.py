from inventory import Inventory
import locale
import numpy as np
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
        self.mass_taken = []

    def __str__(self):
        return str(self.name) + ' ' + str(self.payload_mass) + ' ' + \
        str(self.payload_volume) + ' ' + str(self.mass) + ' ' +\
        str(self.base_costs) + ' ' + str(self.fuel_to_weight)

    def take(self, item):
        self.inventory.add(item)
        self.payload_mass = self.payload_mass - item.mass
        self.mass_taken.append(item.mass)
        self.payload_volume = self.payload_volume - item.volume
        
    def remove(self, item):
        self.inventory.remove(item)
        self.payload_mass = self.payload_mass + item.mass
        self.mass_taken.remove(item.mass)
        self.payload_volume = self.payload_volume + item.volume

    def fit(self, item):
        if item.mass < self.payload_mass and item.volume < self.payload_volume:
            return True

    def total_costs(self):
        total_fuel = (self.mass+sum(self.mass_taken))*(self.fuel_to_weight/(1-self.fuel_to_weight))
        #self.total_costs = np.ceil(self.total_fuel * 1000) + self.base_costs
        total_costs = np.ceil(total_fuel * 1000) + self.base_costs
        return total_costs
