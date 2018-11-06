
class Cargo(object):
    def __init__(self, parcel_id, mass, volume, mass_per_vol):
        self.parcel_id = parcel_id
        self.mass = mass
        self.volume = volume
        self.mass_per_vol = mass_per_vol

    def __str__(self):
        return str(self.parcel_id) + ' ' + str(self.mass) + ' ' + str(self.volume) + ' ' + str(self.mass_per_vol)
