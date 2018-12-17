import random
import numpy as np
import csv
import locale
from space_craft import Spacecraft
from cargo import Cargo
from inventory import Inventory
import sys
import timeit
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class spacefreight():
    def __init__(self, list, spacelist):

        # call the files that are needed for the operation
        self.ships = self.load_ships(f"{spacelist}.txt")
        self.cargo = self.load_cargo(f"CargoLists/Cargo{list}.csv")
        self.ship_list = []

    def __str__(self):
        s = ""
        for i in self.ships:
            s+= str(i.name) + " " + str(len(i.inventory.inventory)) + "\n"
            for n in i.inventory.inventory:
                s+= str(n)+"\n"
            s+="\n"
        return(s)

    def load_cargo(self, filename):
        list_cargo = []
        # read cargo file, include information of parcels
        with open(filename) as csv_data:
                reader = csv.reader(csv_data, delimiter=',')
                next(reader)
                # sort list
                val_sorted = sorted(reader, key = lambda\
                    x:float(x[2])/float(x[1]), reverse=False)
                for line in val_sorted:
                    parcel_id = line[0]
                    mass = float(line[1])
                    volume = float(line[2])
                    cargo_data = Cargo(parcel_id, mass, volume)
                    list_cargo.append(cargo_data)
        return list_cargo

    def load_ships(self, filename):
        list_ships = []
        # read cargo file, include information of parcels
        with open(filename) as csv_data:
                reader = csv.reader(csv_data, delimiter=',')
                # sort list
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

    # algorithm that finds solutions, iterates over all ships and cargo, greedy
    def calculate_greedy(self, ship, item):
        count_cargo = 0
        count_ships = 0
        list_amount = []
        while count_ships < len(self.ships): # iterates over all ships
            current_ship = self.ships[ship%len(self.ships)]
            cur = current_ship
            y = 0
            aantal = 0
            while count_cargo < len(self.cargo):  # iterates over all cargo
                current_cargo = self.cargo[item%len(self.cargo)]
                # next item if it doesn't fit
                if not cur.fit(current_cargo):
                    item+=1
                    count_cargo+=1
                # check if cargo already placed
                elif current_cargo in self.ship_list:
                    item+=1
                    count_cargo+=1
                else: # if cargo fits, append
                    cur.take(current_cargo)
                    self.ship_list.append(current_cargo)
                    item+=1
                    count_cargo+=1
                    aantal+=1
            count_cargo = 0
            ship+=1
            count_ships+=1
    # random algorithm
    def random_fill(self):
        cargo_to_fill=round(len(self.cargo))
        for cargo_index in range(0,cargo_to_fill):
            current_cargo = self.cargo[cargo_index]
            ship_index= random.randint(0, len(self.ships)-1)
            current_ship=self.ships[ship_index]
            if current_ship.fit(current_cargo):
                if not current_cargo in self.ship_list:
                    current_ship.take(current_cargo)
                    self.ship_list.append(current_cargo)

    # swap random cargo
    def swap(self):
        ship1_count = random.randint(0, (len(self.ships)-1))
        ship2_count = random.randint(0, (len(self.ships)-1))
        if ship1_count == ship2_count:
            ship2_count = ((ship2_count+1)%len(self.ships))
        ship1 = self.ships[ship1_count]
        ship2 = self.ships[ship2_count]
        p1_1len = len(ship1.inventory.inventory)
        i = random.randint(0, (len(ship1.inventory.inventory)-1))
        j = random.randint(0, (len(ship2.inventory.inventory)-1))
        p1_1 = ship1.inventory.inventory[i]
        p1_2 = ship2.inventory.inventory[j]
        ship1.remove(p1_1)
        ship2.remove(p1_2)
        if ship1.fit(p1_2) == True and ship2.fit(p1_1) == True:
            ship1.take(p1_2)
            ship2.take(p1_1)
        else:
            ship1.take(p1_1)
            ship2.take(p1_2)
        p1_1len = len(ship1.inventory.inventory)
        p1_2len = len(ship2.inventory.inventory)

    def count(self):
        return len(self.ship_list)

    # print info costs, spacecrafts, parcels
    def info(self):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        for i in self.ships:
            print(i)
            for j in i.inventory.inventory:
                print(j)
        total_costs = []
        for spacecraft in self.ships:
            print(spacecraft)
            total_costs.append(spacecraft.total_costs())
            print('The total costs for this ship is: ', \
                 locale.currency(spacecraft.total_costs(), grouping = True))
        print()
        print('The total transport costs are:',\
              locale.currency(sum(total_costs), grouping = True))
        print('The costs per parcel are:',\
              locale.currency(sum(total_costs)/len(self.ship_list), grouping = True))
        type = 0
        while type <= len(self.ship_list):
            current_cargo = self.cargo[type]
            if not current_cargo in self.ship_list:
                print(current_cargo.parcel_id)
            type+=1

    def cost(self):
        total_costs = []
        for spacecraft in self.ships:
            total_costs.append(spacecraft.total_costs())
        return sum(total_costs)

    def space_list_number(self):
        total_cargo_mass = []
        total_cargo_volume = []
        for i in self.cargo:
            total_cargo_mass.append(i.mass)
            total_cargo_volume.append(i.volume)
        sum_total_cargo_mass = sum(total_cargo_mass)
        sum_total_cargo_volume = sum(total_cargo_volume)
        number_ships = 100
        number_spaceships = {}
        for i in self.ships:
            massa_ships = sum_total_cargo_mass/i.payload_mass
            volume_ships = sum_total_cargo_volume/i.payload_volume
            if massa_ships > volume_ships:
                number_spaceships[i.name]= massa_ships
            else:
                number_spaceships[i.name] = volume_ships
            if number_ships > number_spaceships[i.name]:
                number_ships = number_spaceships[i.name]
        mass_ship = sum_total_cargo_mass/number_ships
        volume_ship = sum_total_cargo_volume/number_ships

        for i in self.ships:
            if i.payload_mass == mass_ship or i.payload_volume == volume_ship:
                j = 0
                file = open('spacecraft_use.txt','w')
                while j < number_ships:
                    file.write(i.name)
                    file.write(str(j))
                    file.write(",")
                    file.write(i.nation)
                    file.write(",")
                    file.write(str(i.payload_mass))
                    file.write(",")
                    file.write(str(i.payload_volume))
                    file.write(",")
                    file.write(str(i.mass))
                    file.write(",")
                    file.write(str(i.base_costs))
                    file.write(",")
                    file.write(str(i.fuel_to_weight))
                    file.write("\n")
                    j+=1
                file.close()

if __name__ == "__main__":
    if sys.argv[1]=="spaceship" or sys.argv[1]=='all':
        space_freight = spacefreight(sys.argv[2],sys.argv[3])
        labels= []
        for i in space_freight.ships:
            plt.bar(i.payload_volume, i.payload_mass, label=i.name)
        plt.title('Ship information')
        plt.xlabel('volume(m^3)')
        plt.ylabel('massa(kg)')
        plt.legend(loc='upper center')
        plt.show()

    print('Argument List:', str(sys.argv))

    space_freight = spacefreight(sys.argv[2],sys.argv[3])
    space_freight.space_list_number()

    if sys.argv[1]=="greedy" or sys.argv[1]=='all':
        start = timeit.default_timer()
        count_cargo = 0
        cost = 100000000000000000
        best_nr_parcel_packed = 0
        space_freight = spacefreight(sys.argv[2], 'spacecraft_use')
        for ship_index in range(0,len(space_freight.ships)):
            for item_index in range(0,len(space_freight.cargo)):
                space_freight = spacefreight(sys.argv[2],'spacecraft_use')
                space_freight.calculate_greedy(ship_index, item_index)
                if space_freight.count() >= best_nr_parcel_packed:
                    if space_freight.cost() < cost:
                        print('aantal parcels mee: ', space_freight.count())
                        print('kosten: ', space_freight.cost())
                        print(space_freight)
                        print()
                        cost = space_freight.cost()
                        best_nr_parcel_packed = space_freight.count()
                    elif space_freight.count() > best_nr_parcel_packed:
                        cost = space_freight.cost()
        stop = timeit.default_timer()
        print('Time: ', (stop - start))


    if sys.argv[1]=="hill_with_outliers" or sys.argv[1]=='all':
        start = timeit.default_timer()
        best_nr_parcel_packed = 0
        k = 0
        cost = 100000000000000000
        cost_plot = []
        count_plot = []
        while k < 100:
            space_freight = spacefreight(sys.argv[2],'spacecraft_use')
            z = 0
            while z < 100:
                space_freight.random_fill()
                i = 0
                while i < 10:
                     space_freight.swap()
                     i+=1
                z+=1
                space_freight.random_fill()
            if space_freight.count() >= best_nr_parcel_packed:
                if space_freight.cost() < cost:
                    print('aantal parcels mee: ', space_freight.count())
                    print('kosten: ', space_freight.cost())
                    print(space_freight)
                    print()
                    cost = space_freight.cost()
                    best_nr_parcel_packed = space_freight.count()
                    cost_plot.append(cost)
                    count_plot.append(best_nr_parcel_packed)
                    ship_information = space_freight.ships
                elif space_freight.count() > best_nr_parcel_packed:
                    cost = space_freight.cost()
                    cost_plot.append(cost)
                    count_plot.append(best_nr_parcel_packed)
                    ship_information = space_freight.ships
            k+=1
        stop = timeit.default_timer()
        print('Time: ', (stop - start))
        for i in ship_information:
            print(i.name)
            print(len(i.inventory.inventory))
            plt.bar(i.name, len(i.inventory.inventory))
        title = sys.argv[2]
        plt.title(title)
        plt.xlabel('Verne_ATV')
        plt.xticks([])
        plt.ylabel('Amount of parcels')
        plt.show()
        for i in ship_information:
            print(i.name)
            print(i.total_costs())
            plt.bar(i.name, i.total_costs())
        title = sys.argv[2]
        plt.title(title)
        plt.xlabel('Verne_ATV')
        plt.xticks([])
        plt.ylabel('Costs (*100.000.000 $)')
        plt.show()

    if sys.argv[1]=="random" or sys.argv[1]=='all':
        start = timeit.default_timer()
        count_cargo = 0
        i = 0
        cost = 100000000000000000
        best_nr_parcel_packed = 0
        while i < 100000:
            space_freight = spacefreight(sys.argv[2],'spacecraft_use')
            space_freight.random_fill()
            if space_freight.count() >= best_nr_parcel_packed:
                random_cost.append(space_freight.cost())
                random_count.append(space_freight.count())
                if space_freight.cost() < cost:
                    print('aantal parcels mee: ', space_freight.count())
                    print('kosten: ', space_freight.cost())
                    print(space_freight)
                    print()
                    cost = space_freight.cost()
                    best_nr_parcel_packed = space_freight.count()
                elif space_freight.count() > best_nr_parcel_packed:
                    cost = space_freight.cost()
            i+=1

        stop = timeit.default_timer()
        print('Time: ', (stop - start))

    if sys.argv[1]=="all_algoritmes":
        start = timeit.default_timer()
        count_cargo = 0
        i = 0
        cost = 100000000000000000
        best_nr_parcel_packed = 0
        cost_plot = []
        count_plot = []
        while i < 100:
            space_freight = spacefreight(sys.argv[2],'spacecraft_use')
            for ship_index in range(0,len(space_freight.ships)):
                for item_index in range(0,len(space_freight.cargo)):
                    space_freight = spacefreight(sys.argv[2],'spacecraft_use')
                    space_freight.calculate_greedy(ship_index, item_index)
                    cost_plot.append(space_freight.cost())
                    count_plot.append(space_freight.count())
                    if space_freight.count() >= best_nr_parcel_packed:
                        if space_freight.cost() < cost:
                            print('aantal parcels mee: ', space_freight.count())
                            print('kosten: ', space_freight.cost())
                            print(space_freight)
                            print()
                            cost = space_freight.cost()
                            best_nr_parcel_packed = space_freight.count()
                        elif space_freight.count() > best_nr_parcel_packed:
                            cost = space_freight.cost()
        i+=1

        start = timeit.default_timer()
        best_nr_parcel_packed = 0
        k = 0
        cost = 100000000000000000
        hill1_cost = []
        hill1_count = []
        while k < 100000:
            space_freight = spacefreight(sys.argv[2],'spacecraft_use')
            z = 0
            while z < 100:
                space_freight.random_fill()
                i = 0
                while i < 10:
                     space_freight.swap()
                     i+=1
                z+=1
                space_freight.random_fill()
                hill1_cost.append(cost)
                hill1_count.append(best_nr_parcel_packed)
            if space_freight.count() >= best_nr_parcel_packed:
                if space_freight.cost() < cost:
                    print('aantal parcels mee: ', space_freight.count())
                    print('kosten: ', space_freight.cost())
                    print(space_freight)
                    print()
                    cost = space_freight.cost()
                    best_nr_parcel_packed = space_freight.count()
                    hill1_cost.append(cost)
                    hill1_count.append(best_nr_parcel_packed)
                elif space_freight.count() > best_nr_parcel_packed:
                    cost = space_freight.cost()
                    hill1_cost.append(cost)
                    hill1_count.append(best_nr_parcel_packed)
            k+=1
        stop = timeit.default_timer()
        print('Time: ', (stop - start))

        start = timeit.default_timer()
        count_cargo = 0
        i = 0
        cost = 100000000000000000
        best_nr_parcel_packed = 0
        random_cost = []
        random_count = []
        while i < 100000:
            space_freight = spacefreight(sys.argv[2],'spacecraft_use')
            space_freight.random_fill()
            if space_freight.count() >= best_nr_parcel_packed:
                random_cost.append(space_freight.cost())
                random_count.append(space_freight.count())
                if space_freight.cost() < cost:
                    print('aantal parcels mee: ', space_freight.count())
                    print('kosten: ', space_freight.cost())
                    print(space_freight)
                    print()
                    cost = space_freight.cost()
                    best_nr_parcel_packed = space_freight.count()
                elif space_freight.count() > best_nr_parcel_packed:
                    cost = space_freight.cost()
            i+=1
        stop = timeit.default_timer()
        print('Time: ', (stop - start))

        #plot scatterplot with all found solutions, for every algorithm
        title = sys.argv[1]
        list = sys.argv[2]
        plt.title(title + " " + list)
        plt.xlabel('Costs')
        plt.ylabel('Amount of Parcels')
        plt.plot(cost_plot, count_plot, 'ro')
        plt.plot(hill1_cost, hill1_count, 'go')
        plt.plot(random_cost, random_count, 'ko')
        red_patch = mpatches.Patch(color='red', label='Greedy')
        green_patch = mpatches.Patch(color='green', label='Hill without outliers')
        black_patch = mpatches.Patch(color='black', label='Random')
        plt.legend(handles=[red_patch, green_patch, black_patch])
        plt.axis([(min(random_cost)-1000000), (max(cost_plot)+1000000),\
         (min(count_plot)-5), (max(count_plot)+10)])
        plt.show()
