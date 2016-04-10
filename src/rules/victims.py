# victims.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.victim import Victim


class Victims(Skeleton):

    def __init__(self):
        self.json_file_name = "victims.json"
        self.victims = list()

    def sort(self):
        self.victims.sort(key=lambda x: x.isk_lost * x.ships_lost, reverse=True)

    def process_km(self, killmail):
        isk_lost = killmail['zkb']['totalValue']
        victim_id = killmail['victim']['characterID']
        victim_name = killmail['victim']['characterName']

        if victim_name != "":
            victims = filter(
                lambda x: x.character_name == victim_name,
                self.victims
            )

            if len(victims):
                victim_index = self.victims.index(victims[0])
                self.victims[victim_index].ships_lost += 1
                self.victims[victim_index].isk_lost += isk_lost
            else:
                self.victims.append(
                    Victim(victim_id, victim_name, 1, isk_lost)
                )
