#Class die een inventory maakt voor de schepen 
from cargo import Cargo
class Inventory(object):
    def __init__(self):
        self.inventory = []
    def add(self, item):
        self.inventory.append(item)
    def remove(self, item):
        self.inventory.remove(item)
    def __str__(self):
        item = ""
        for i in self.inventory:
            item = i.parcel_id
            #  +":" + " " + i.description
        return item
