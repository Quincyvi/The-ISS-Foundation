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

class spacefreight():
    def __init__(self, list, spacelist):

        # call the files that are needed for the operation
        self.ships = self.load_ships(f"{spacelist}.txt")
        self.cargo = self.load_cargo(f"CargoLists/Cargo{list}.csv")
        self.ship_list = []

    def __str__(self):
        # s="============= ships:\n"
        # for i in self.ships:
        #     s+=str(i)
        #     s+=str(len(i.inventory.inventory))
        # s+="============= cargo:\n"
        # for i in self.cargo:
        #     s+=str(i)
        # return s
        s = ""
        for i in self.ships:
            s+= str(i.name) + " " + str(len(i.inventory.inventory)) + "\n"
        return(s)

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
        count_cargo = 0
        count_ships = 0
        list_amount = []
        while count_ships < len(self.ships): # gaat over alle schepen
            current_ship = self.ships[ship%len(self.ships)]
            cur = current_ship
            y = 0
            aantal = 0
            while count_cargo < len(self.cargo):
                current_cargo = self.cargo[item%len(self.cargo)]
                if not cur.fit(current_cargo):
                    item+=1
                    count_cargo+=1
                elif current_cargo in self.ship_list:
                    item+=1
                    count_cargo+=1
                else: # als het wel ingeladen kan worden:
                    cur.take(current_cargo)
                    self.ship_list.append(current_cargo)
                    item+=1
                    count_cargo+=1
                    aantal+=1
            count_cargo = 0
            ship+=1
            count_ships+=1

    def random_fill(self): # maak random indeling
        # print("random_fill")
        cargo_to_fill=round(len(self.cargo)) # fill half, just a test
        # print("fill first:",cargo_to_fill," parcels")
        for cargo_index in range(0,cargo_to_fill):
            # print("try fit:",cargo_index)
            current_cargo = self.cargo[cargo_index]
            ship_index= random.randint(0, len(self.ships)-1)
            current_ship=self.ships[ship_index]
            if current_ship.fit(current_cargo):
                if not current_cargo in self.ship_list:
                    current_ship.take(current_cargo)
                    # print("  parcel:",cargo_index," in:", ship_index)
                    self.ship_list.append(current_cargo)

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
            # print("het kan, swap ",p1_2," met ",p1_1)
            # print("ship1:",ship1)
            # print("ship2:",ship2)
        else:
            # print('het kan niet')
            ship1.take(p1_1)
            ship2.take(p1_2)

        p1_1len = len(ship1.inventory.inventory)
        p1_2len = len(ship2.inventory.inventory)

    def count(self):
        return len(self.ship_list)

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
            # print(spacecraft)
            total_costs.append(spacecraft.total_costs())
            # print('The total costs for this ship is: ', \
                 # locale.currency(spacecraft.total_costs(), grouping = True))
        return sum(total_costs)

    def delete_outliners(self):
        total_ship_mass = []
        total_ship_volume = []
        total_cargo_mass = []
        total_cargo_volume = []
        cargo_list_length = 0
        for i in self.ships:
            total_ship_mass.append(i.payload_mass)
            total_ship_volume.append(i.payload_volume)
        for i in self.cargo:
            total_cargo_mass.append(i.mass)
            total_cargo_volume.append(i.volume)

        while sum(total_ship_mass) < sum(total_cargo_mass) or sum(total_ship_volume) < sum(total_cargo_volume):
            k = total_cargo_volume.pop(random.randrange(len(total_cargo_volume)))
            for i in self.cargo:
                if k == i.volume:
                    self.cargo.remove(i)
                    total_cargo_mass.remove(i.mass)
        return len(self.cargo)

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
        best_space_ship = []
        best_space_ship.append(number_ships)
        mass_ship = sum_total_cargo_mass/number_ships
        volume_ship = sum_total_cargo_volume/number_ships

        for i in self.ships:
            if i.payload_mass == mass_ship or i.payload_volume == volume_ship:
                j = 0
                file = open('spacecraft_use.txt','w')
                while j < number_ships:
                    file.write(i.name)
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

    def space_list_cost(self):
        cost_pp_spaceships = {}
        cost = 100000000000000
        for i in self.ships:
            cost_pp_ships = int(i.total_costs())/len(i.inventory.inventory)
            cost_pp_spaceships[i.name] = cost_pp_ships
            if cost_pp_spaceships[i.name] < cost:
                cost = cost_pp_spaceships[i.name]
        best_space_ship = []
        best_space_ship.append(cost)
        # print(cost)
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
        for i in self.ships:
            if i.total_costs == cost*len(i.inventory.inventory):
                j = 0
                file = open('spacecraft_cost.txt','w')
                while j < number_ships:
                    file.write(i.name)
                    file.write(j)
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
    print('Argument List:', str(sys.argv))
    cost_plot_g = []
    count_plot_g = []
    cost_plot_h = []
    count_plot_h = []
    cost_plot_hh = []
    count_plot_hh = []
    cost_plot_r = []
    count_plot_r = []

    if sys.argv[1]=="greedy" or sys.argv[1]=='all':
        start = timeit.default_timer()
        count_cargo = 0
        i = 0
        cost = 100000000000000000
        best_nr_parcel_packed = 0
        cost_plot = []
        count_plot = []
        print("let's Go")
        space_freight = spacefreight(sys.argv[2],sys.argv[3])
        # space_freight.space_list_number()
        for ship_index in range(0,len(space_freight.ships)):
            for item_index in range(0,len(space_freight.cargo)):
                space_freight = spacefreight(sys.argv[2],sys.argv[3])
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
                        # print(space_freight)
        space_freight.space_list_cost()
        space_freight = spacefreight(sys.argv[2],'spacecraft_use')
        stop = timeit.default_timer()
        print('Time: ', (stop - start))

    if sys.argv[1]=="hill" or sys.argv[1]=='all':
        start = timeit.default_timer()
        count_cargo = 0
        best_nr_parcel_packed = 0
        k = 0
        cost = 100000000000000000
        space_freight = spacefreight(sys.argv[2],sys.argv[3])
        space_freight.space_list_number()
        while k < 100:
            space_freight = spacefreight(sys.argv[2],"spacecraft_use")
            if space_freight.delete_outliners() >= count_cargo:
                count_cargo = space_freight.delete_outliners()
                z = 0
                while z < 100:
                    space_freight.random_fill() # start met random indeling
                    # print(space_freight) # print de indeling van space crafts
                    i = 0
                    while i < 10:
                         space_freight.swap()
                         i+=1
                    z+=1
                    space_freight.random_fill()
                    # print(space_freight)
                    cost_plot_h.append(space_freight.cost())
                    count_plot_h.append(space_freight.count())
                if space_freight.count() >= best_nr_parcel_packed:
                    # print(best_nr_parcel_packed)
                    # print(space_freight.cost())
                    if space_freight.cost() < cost:
                        print('aantal parcels mee: ', space_freight.count())
                        print('kosten: ', space_freight.cost())
                        print(space_freight)
                        print()
                        cost = space_freight.cost()
                        best_nr_parcel_packed = space_freight.count()
                        cost_plot.append(cost)
                        count_plot.append(best_nr_parcel_packed)
                    elif space_freight.count() > best_nr_parcel_packed:
                        cost = space_freight.cost()
                        cost_plot.append(cost)
                        count_plot.append(best_nr_parcel_packed)
                        # print(space_freight)
            k+=1
        stop = timeit.default_timer()
        print('Time: ', (stop - start))

    if sys.argv[1]=="hill_with_outliers" or sys.argv[1]=='all':
        best_nr_parcel_packed = 0
        k = 0
        cost = 100000000000000000
        space_freight = spacefreight(sys.argv[2],sys.argv[3])
        space_freight.space_list_number()
        while k < 100:
            space_freight = spacefreight(sys.argv[2],"spacecraft_use")
            z = 0
            while z < 100:
                space_freight.random_fill() # start met random indeling
                # print(space_freight) # print de indeling van space crafts
                i = 0
                while i < 10:
                     space_freight.swap()
                     i+=1
                z+=1
                space_freight.random_fill()
                # print(space_freight)

            if space_freight.count() >= best_nr_parcel_packed:
                # print(best_nr_parcel_packed)
                # print(space_freight.cost())
                cost_plot_hh.append(space_freight.cost())
                count_plot_hh.append(space_freight.count())
                if space_freight.cost() < cost:
                    print('aantal parcels mee: ', space_freight.count())
                    print('kosten: ', space_freight.cost())
                    print(space_freight)
                    print()
                    cost = space_freight.cost()
                    best_nr_parcel_packed = space_freight.count()
                elif space_freight.count() > best_nr_parcel_packed:
                    cost = space_freight.cost()

            k+=1
    if sys.argv[1]=="random" or sys.argv[1]=='all':
        start = timeit.default_timer()
        count_cargo = 0
        i = 0
        cost = 100000000000000000
        best_nr_parcel_packed = 0
        cost_plot = []
        count_plot = []
        while i < 100:
            space_freight = spacefreight(sys.argv[2],sys.argv[3])
            space_freight.random_fill()
            # print(space_freight)
            cost_plot_r.append(space_freight.cost())
            count_plot_r.append(space_freight.count())
            if space_freight.count() >= best_nr_parcel_packed:
                cost_plot.append(space_freight.cost())
                count_plot.append(space_freight.count())
                # print(best_nr_parcel_packed)
                # print(space_freight.cost())
                if space_freight.cost() < cost:
                    print('aantal parcels mee: ', space_freight.count())
                    print('kosten: ', space_freight.cost())
                    print(space_freight)
                    print()
                    cost = space_freight.cost()
                    best_nr_parcel_packed = space_freight.count()
                    # cost_plot.append(space_freight.cost())
                    # count_plot.append(space_freight.count())
                elif space_freight.count() > best_nr_parcel_packed:
                    cost = space_freight.cost()
                    # cost_plot.append(space_freight.cost())
                    # count_plot.append(space_freight.count())
                space_freight.space_list_cost()
                space_freight = spacefreight(sys.argv[2],'spacecraft_use')
            i+=1
        stop = timeit.default_timer()
        print('Time: ', (stop - start))

    # title = sys.argv[1]
    # print(spacefreight)
    # plt.title(title)
    # plt.xlabel('Costs')
    # plt.ylabel('Amount of Parcels')
    # plt.plot(cost_plot, count_plot, 'ro')
    # plt.axis([1465000000, 1468000000, 70, 100])
    # plt.show()

    # list = sys.argv[2]
    # plt.hist(cost_plot)
    # plt.xlabel("Cost")
    # minScore = min([min(cost_plot_g), min(cost_plot_h), min(cost_plot_hh), min(cost_plot_r)])
    # maxScore = max([max(cost_plot_g), max(cost_plot_h), max(cost_plot_hh), max(cost_plot_r)])
    # bins = np.linspace(minScore, maxScore, 100)
    # print(bins)
    # print(cost_plot_h)
    # print(cost_plot_r)
    # print(cost_plot_g)
    # print(cost_plot_hh)
    # plt.hist(cost_plot_g, bins, alpha=0.5, label='g')
    # plt.hist(cost_plot_r, bins, alpha=0.5, label='r')
    # plt.hist(cost_plot_h, bins, alpha=0.5, label='h')
    # # plt.hist(cost_plot_hh, bins, alpha=0.5, label='hh')
    # # plt.hist(count_plot, bins, alpha=0.5, label='y')
    # plt.legend(loc='upper right')
    # plt.show()
    # minCount = min([min(count_plot_g), min(count_plot_h), min(count_plot_hh), min(count_plot_r)])
    # maxCount = max([max(count_plot_g), max(count_plot_h), max(count_plot_hh), max(count_plot_r)])
    # bin = np.linspace(minCount, maxCount, (maxCount-minCount+1))
    # print(bin)
    # plt.hist([count_plot_g,count_plot_r,count_plot_h,count_plot_hh], bin, alpha=0.5, label=['g','r','h','hh'])
    # plt.hist(count_plot_r, bin, alpha=0.5, label='r')
    # plt.hist(count_plot_h, bin, alpha=0.5, label='h')
    # plt.hist(count_plot_hh, bin, alpha=0.5, label='hh')
    # plt.legend(loc='upper right')
    # plt.show()
    # # plt.title(title)
    # plt.ylabel(list)
    # plt.show()

    # plt.hist(count_plot)
    # plt.xlabel("number parcels")
    # plt.title(title)
    # plt.ylabel(list)
    # plt.show()
