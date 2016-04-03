# capitals.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class Capitals(Skeleton):

    def __init__(self):
        self.json_file_name = "capital_kills.json"
        self.most_valuable = list()

    def sort(self):
        self.most_valuable.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        kill_id = killmail['killID']
        isk_destroyed = killmail['zkb']['totalValue']
        victim_ship = killmail['victim']['shipTypeID']
        if victim_ship in [
            19724, 34339, 19722, 34341, 19726, 34343, 19720, 34345,  # Dreads
            23757, 23915, 24483, 23911,  # Carriers
            23919, 22852, 3628, 23913, 3514, 23917,  # Supers
            11567, 671, 3764, 23773,  # Titans
        ]:
            self.most_valuable.append({'kill_id': kill_id, 'destroyed': isk_destroyed})
