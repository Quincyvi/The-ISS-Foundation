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
        ship_list = []
        count_cargo = 0
        count_ships = 0
        list_amount = []
        while count_ships < len(self.ships): # gaat over alle schepen
            self.current_ship = self.ships[ship%len(self.ships)]
            cur = self.current_ship
            y = 0
            aantal = 0
            while count_cargo < len(self.cargo):
                self.current_cargo = self.cargo[item%len(self.cargo)]
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
        if len(ship_list) >= 96:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            start_ships = ship - count_ships
            start_cargo = item % 97
            print('the start number for cargo list = ', start_cargo)
            print('the start number for ship list = ', start_ships)
            print('the max value is: ', len(ship_list))
            total_costs = []
            for spacecraft in self.ships:
                print(spacecraft)
                print('The total costs for this ship is: ', \
                     locale.currency(spacecraft.total_costs(), grouping = True))
            type = 0
            while type <= len(ship_list):
                self.current_cargo = self.cargo[type]
                if not self.current_cargo.parcel_id in ship_list:
                    print(self.current_cargo.parcel_id)
                type+=1
            for i in self.ships:
                print(i)
                for j in i.inventory.inventory:
                    print(j)
                print()

    def random_fill(self): # maak random indeling
        print("random_fill")
        cargo_to_fill=round(len(self.cargo)/2) # fill half, just a test
        print("fill first:",cargo_to_fill," parcels")
        for cargo_index in range(0,cargo_to_fill):
            print("try fit:",cargo_index)
            current_cargo = self.cargo[cargo_index]
            ship_index= random.randint(0, len(self.ships)-1)
            current_ship=self.ships[ship_index]
            if current_ship.fit(current_cargo):
                current_ship.take(current_cargo)
                print("  parcel:",cargo_index," in:", ship_index)

    def swap(self):
        ship1_count = random.randint(0, 3)
        ship2_count = random.randint(0, 3)
        if ship1_count == ship2_count:
            ship2_count = ((ship2_count+1)%len(self.ships))
        ship1 = self.ships[ship1_count]
        ship2 = self.ships[ship2_count]
        p1_1len = len(ship1.inventory.inventory)
        i = random.randint(0, (len(ship1.inventory.inventory)-1))
        j = random.randint(0, (len(ship2.inventory.inventory)-1))
        p1_1 = ship1.inventory.inventory[i]
        p1_2 = ship2.inventory.inventory[j]
        ship1.inventory.remove(p1_1)
        ship2.inventory.remove(p1_2)
        if ship1.fit(p1_2) == True and ship2.fit(p1_1) == True:
            ship1.take(p1_2)
            ship2.take(p1_1)
            print("het kan, swap ",p1_2," met ",p1_1)
            print("ship1:",ship1)
            print("ship2:",ship2)
        else:
            print('het kan niet')
            ship1.take(p1_1)
            ship2.take(p1_2)

        p1_1len = len(ship1.inventory.inventory)
        # p1=ship1.get_random_parcel()
        # p2=ship2.get_random_parcel()
        # ship1.remove(p1)
        # ship2.remove(p2)
        # if ship1.fit(p2) and ship2.fit(p1):
        #     ship1.add(p2)
        #     ship2.add(p1)
        #     if score<oud_score:
        #         ship1.remove(p2)
        #         ship2.remove(p1)
        #         ship1.add(p1)
        #         ship2.add(p2)


if __name__ == "__main__":
    ship = 1
    item = 37
    space_freight = spacefreight('ListTest')
    #space_freight.calculate_greedy(ship, item)
    space_freight.random_fill() # start met random indeling
    print(space_freight) # print de indeling van space crafts
    i = 0
    while i < 10:
         space_freight.swap()
         i+=1
