# topship.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import csv
from skeleton import Skeleton
from statsconfig import StatsConfig


class TopShip(Skeleton):

    def __init__(self):
        self.json_file_name = "top_ship.json"
        self.ships_destroyed = list()
        self.isk_destroyed = list()

        with open('typeIDs.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.items = {int(rows[0]):rows[1] for rows in reader}

    def sort(self):
        self.ships_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)
        self.isk_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)

    def preprocess_output(self):
        dictionary = super(self.__class__, self).preprocess_output()
        del dictionary["items"]
        return dictionary

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        for attacker in killmail['attackers']:
            attacker_name = attacker['characterName']
            attacker_corp = attacker['corporationID']
            attacker_ship = attacker['shipTypeID']

            if attacker_ship != 0 and attacker_ship not in [670, 33328]:  # ignore unknown and capsules
                if attacker_name != "" and attacker_corp in StatsConfig.CORP_IDS:
                    all_ships_destroyed = filter(
                        lambda x: x.get('name') == self.items[attacker_ship],
                        self.ships_destroyed
                    )
                    all_isk_destroyed = filter(
                        lambda x: x.get('name') == self.items[attacker_ship],
                        self.isk_destroyed
                    )

                    if len(all_ships_destroyed):
                        ship_index = self.ships_destroyed.index(all_ships_destroyed[0])
                        self.ships_destroyed[ship_index]['destroyed'] += 1
                    else:
                        self.ships_destroyed.append({'name': self.items[attacker_ship], 'destroyed': 1})

                    if len(all_isk_destroyed):
                        ship_index = self.isk_destroyed.index(all_isk_destroyed[0])
                        self.isk_destroyed[ship_index]['destroyed'] += isk_destroyed
                    else:
                        self.isk_destroyed.append({'name': self.items[attacker_ship], 'destroyed': isk_destroyed})
