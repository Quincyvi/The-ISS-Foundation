import random
import numpy as np
import csv
import locale
from space_craft import Spacecraft
from cargo import Cargo
from inventory import Inventory
# import matplotlib.pyplot as plt

class spacefreight():
    def __init__(self, list):

        # call the files that are needed for the operation
        self.ships = self.load_ships(f"spacecraft.txt")
        self.cargo = self.load_cargo(f"CargoLists/Cargo{list}.csv")

    def load_cargo(self, filename):
        list_cargo = []
        with open(filename) as csv_data:
                reader = csv.reader(csv_data, delimiter=',')
                next(reader)
                val_sorted = sorted(reader, key = lambda\
                    x:float(x[2])/float(x[1]), reverse=False)
                    #x:float(x[2]), reverse=False)
                for line in val_sorted:
                    parcel_id = line[0]
                    mass = float(line[1])
                    volume = float(line[2])
                    # mass_per_vol = mass / volume
                    cargo_data = Cargo(parcel_id, mass, volume)
                    list_cargo.append(cargo_data)
                    # print(cargo_data)
                    # print(mass, volume)
        return list_cargo

    def load_ships(self, filename):
        list_ships = []
        with open(filename) as csv_data:
                reader = csv.reader(csv_data, delimiter=',')
                val_sorted = sorted(reader, key = lambda\
                                    x:float(x[3])/float(x[2]), reverse=False)
                for line in val_sorted:
                    ship_name = line[0]
                    ship_location = line[1]
                    ship_pay_mass = int(line[2])
                    ship_pay_vol = float(line[3])
                    ship_mass = int(line[4])
                    ship_base_costs = line[5]
                    costs = ship_base_costs.split('M')
                    ship_base_costs = int(costs[0]) * 1000000
                    ship_fuel = float(line[6])
                    ship_data = Spacecraft(ship_name, ship_location,
                                           ship_pay_mass, ship_pay_vol,
                                           ship_mass, ship_base_costs,
                                           ship_fuel)
                    list_ships.append(ship_data)
        return list_ships

    def calculate_greedy(self, ship, item):
        for ship_standard in self.ships:
            ship_standard_payload = ship_standard.payload_mass
        ship_list = []
        count_cargo = 0
        count_ships = 0
        list_amount = []
        while count_ships < len(self.ships): # gaat over alle schepen
            self.current_ship = self.ships[ship%4]
            cur = self.current_ship
            # print(cur)
            y = 0
            aantal = 0
            while count_cargo < len(self.cargo):
                self.current_cargo = self.cargo[item%97]
                if cur.payload_mass < self.current_cargo.mass or\
                   cur.payload_volume < self.current_cargo.volume:
                    item+=1
                    count_cargo+=1
                elif self.current_cargo.parcel_id in ship_list:
                    item+=1
                    count_cargo+=1
                else: # als het wel ingeladen kan worden:
                    cur.take(self.current_cargo)
                    ship_list.append(self.current_cargo.parcel_id)
                    item+=1
                    count_cargo+=1
                    aantal+=1
            count_cargo = 0
            ship+=1
            count_ships+=1
        if len(ship_list) >= 0:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            start_ships = ship - count_ships
            start_cargo = item % 97
            print('the start number for cargo list = ', start_cargo)
            print('the start number for ship list = ', start_ships)
            print('the max value is: ', len(ship_list))
            # print(ship_list)
            total_costs = []
            for spacecraft in self.ships:
                print(spacecraft)
                print('The total costs for this ship is: ', \
                     locale.currency(spacecraft.total_costs(), grouping = True))
            type = 0
            while type <= 96:
                self.current_cargo = self.cargo[type]
                if not self.current_cargo.parcel_id in ship_list:
                    print(self.current_cargo.parcel_id)
                type+=1
            # start_ships = ship - count_ships
            # start_cargo = item % 97
            # print('the start number for cargo list = ', start_cargo)
            # print('the start number for ship list = ', start_ships)
            # print('the max value is: ', len(ship_list))
            # # print(ship_list)
            # total_costs = 0
            # for spacecraft in self.ships:
            #     print(spacecraft)
            #     total_payload_weight = ship_standard_payload - spacecraft.payload_mass
            #     payload_fuel_mass = (spacecraft.mass + total_payload_weight)\
            #                         * spacecraft.fuel_to_weight
            #     ship_fuel_mass = (spacecraft.mass + total_payload_weight\
            #                      + payload_fuel_mass) * spacecraft.fuel_to_weight
            #     total_ship_fuel_mass = (spacecraft.mass + total_payload_weight)\
            #                            * (spacecraft.fuel_to_weight / \
            #                            (1 - spacecraft.fuel_to_weight))
            #     ship_costs = np.ceil(total_ship_fuel_mass * 1000)
            #     print('The total fuel mass is: {} kg'.format(total_ship_fuel_mass))
            #     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            #     costs_per_ship = spacecraft.base_costs + ship_costs
            #     total_costs += costs_per_ship
            #     print(locale.currency(costs_per_ship, grouping = True))
            #     print()
            # print('The total costs for the operation is: ', locale.currency(total_costs, grouping = True))
            # cost_per_parcel = total_costs / len(ship_list)
            # print('The costs per parcel is: ', locale.currency(cost_per_parcel, grouping = True))
            # print()
            # print()
            # type = 0
            # print(len(ship_list))
            # while type <= 96:
            #     self.current_cargo = self.cargo[type]
            #     if not self.current_cargo.parcel_id in ship_list:
            #         print(self.current_cargo.parcel_id)
            #     type+=1

    def calculate_hill_climben(self, ship, item):
        for ship_standard in self.ships:
            ship_standard_payload = ship_standard.payload_mass
        ship_list = []
        count_cargo = 0
        count_ships = 0
        list_amount = []
        while count_ships < len(self.ships): # gaat over alle schepen
            self.current_ship = self.ships[ship%4]
            cur = self.current_ship
            y = 0
            aantal = 0
            while count_cargo < len(self.cargo):
                self.current_cargo = self.cargo[item%97]
                if cur.payload_mass < self.current_cargo.mass or\
                   cur.payload_volume < self.current_cargo.volume:
                    item+=1
                    count_cargo+=1
                # elif self.current_cargo.volume > self.cargo[(item+1)%97].volume\
                #      and self.current_cargo.mass > self.cargo[(item+1)%97].mass:
                #     item+=1
                #     count_cargo+=1
                elif self.current_cargo.parcel_id in ship_list:
                    item+=1
                    count_cargo+=1
                else: # als het wel ingeladen kan worden:
                    cur.take(self.current_cargo)
                    ship_list.append(self.current_cargo.parcel_id)
                    item+=1
                    count_cargo+=1
                    aantal+=1
            if cur.payload_volume < self.ships[(ship+1)%4].payload_volume and \
               cur.payload_mass < self.ships[(ship+1)%4].payload_mass:
                ship+=1
                count_cargo = 0
            else:
                count_cargo = 0
                count_ships+=1
        if len(ship_list) >= 96:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            start_ships = ship - count_ships
            start_cargo = item % 97
            print('the start number for cargo list = ', start_cargo)
            print('the start number for ship list = ', start_ships)
            print('the max value is: ', len(ship_list))
            # print(ship_list)
            total_costs = []
            for spacecraft in self.ships:
                print(spacecraft)
                print('The total costs for this ship is: ', \
                     locale.currency(spacecraft.total_costs(), grouping = True))
            type = 0
            while type <= 96:
                self.current_cargo = self.cargo[type]
                if not self.current_cargo.parcel_id in ship_list:
                    print(self.current_cargo.parcel_id)
                type+=1

if __name__ == "__main__":
    ship = 0
    item = 0
    while ship < 4:
        while item < 100:
            space_freight = spacefreight('ListTest')
            space_freight.calculate_hill_climben(ship, item)
            item+=1
        item=0
        ship+=1

## clear & herhaal calculate, observaties ergens saven, enkel de beste uitkomst.
