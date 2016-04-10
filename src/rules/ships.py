# ships.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import csv
from skeleton import Skeleton
from statsconfig import StatsConfig
from models.ship import Ship


class Ships(Skeleton):

    def __init__(self):
        self.json_file_name = "ships.json"
        self.ships = list()

        with open('typeIDs.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.type_ids = {int(rows[0]): rows[1] for rows in reader}

    def sort(self):
        self.ships.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

    def preprocess_output(self):
        dictionary = super(self.__class__, self).preprocess_output()
        del dictionary["type_ids"]
        return dictionary

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        for attacker in killmail['attackers']:
            attacker_name = attacker['characterName']
            attacker_corp = attacker['corporationID']
            attacker_ship = attacker['shipTypeID']

            # Ignore unknown and capsules
            if attacker_ship != 0 and attacker_ship not in [670, 33328]:
                if attacker_name != "" and attacker_corp in StatsConfig.CORP_IDS:
                    ships = filter(
                        lambda x: x.ship_type_id == attacker_ship,
                        self.ships
                    )

                    if len(ships):
                        ship_index = self.ships.index(ships[0])
                        self.ships[ship_index].ships_destroyed += 1
                        self.ships[ship_index].isk_destroyed += isk_destroyed
                    else:
                        self.ships.append(
                            Ship(
                                attacker_ship,
                                self.type_ids[attacker_ship],
                                1,
                                isk_destroyed
                            )
                        )
