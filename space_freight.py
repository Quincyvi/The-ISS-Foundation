import random
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
                    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                    ship_base_costs = locale.currency(int(costs[0]) * 1000000,
                                                      grouping=True)
                    ship_fuel = float(line[6])
                    ship_data = Spacecraft(ship_name, ship_location,
                                           ship_pay_mass, ship_pay_vol,
                                           ship_mass, ship_base_costs,
                                           ship_fuel)
                    list_ships.append(ship_data)
                    # print(ship_data)
        return list_ships

    def take(self, item):
        self.current_ship.inventory.add(item)

    def calculate(self, ship, item):
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
                    cur.payload_mass -= self.current_cargo.mass
                    cur.payload_volume -= self.current_cargo.volume
                    item+=1
                    count_cargo+=1
                    aantal+=1
                    space_freight.take(self.current_cargo)
                    ship_list.append(self.current_cargo.parcel_id)
            count_cargo = 0
            ship+=1
            count_ships+=1
            # print(cur)
        if len(ship_list) >= 96:
            start_ships = ship - count_ships
            start_cargo = item % 97
            print('the start number for cargo list = ', start_cargo)
            print('the start number for ship list = ', start_ships)
            print('the max value is: ', len(ship_list))
            # print(ship_list)
            print()

        # while i < len(self.cargo): # gaat over alle schepen
        #     self.current_cargo = self.cargo[i]
        #     parcel = self.current_cargo
        #     print(parcel/6)
        #     y = 0
        #     while x < len(self.ships):
        #         self.current_ships = self.ships[x]
        #         cur = self.current_ship
        #         # Upperbound
        #         if cur.payload_mass < self.current_cargo.mass or\
        #            cur.payload_volume < self.current_cargo.volume:
        #             i+=1 # volgende parcel
        #             if cur.payload_mass < self.current_cargo.mass or\
        #                cur.payload_volume < self.current_cargo.volume:
        #                 print(cur) # print huidige data: wat is er over aan mass & volume
        #                 print(cur.name + " will transport " + str(y) + " parcels")
        #                 print() ##
        #                 break
        #         else: # als het wel ingeladen kan worden:
        #             cur.payload_mass -= self.current_cargo.mass
        #             cur.payload_volume -= self.current_cargo.volume
        #         space_freight.take(self.current_cargo)
        #         print(cur.inventory)
        #         x+=1 # volgende item
        #         y+=1 # volgende item voor dit schip
        # print("Total amount of parcels:", x) # hoe vaak de loop in
if __name__ == "__main__":
    ship = 0
    item = 0
    while ship < 4:
        while item < 100:
            space_freight = spacefreight('List1')
            space_freight.calculate(ship, item)
            item+=1
        item=0
        ship+=1

## clear & herhaal calculate, observaties ergens saven, enkel de beste uitkomst.
