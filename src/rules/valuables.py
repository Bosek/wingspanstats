# valuables.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.kill import Kill


class Valuables(Skeleton):

    def __init__(self):
        self.json_file_name = "valuables.json"
        self.kills = list()

    def sort(self):
        self.kills.sort(key=lambda x: x.value, reverse=True)

    def process_km(self, killmail):
        kill_id = killmail['killID']
        character_id = killmail['victim']['characterID']
        character_name = killmail['victim']['characterName']
        ship_type_id = killmail['victim']['shipTypeID']
        solar_system_id = killmail['solarSystemID']
        date = killmail['killTime']
        isk_destroyed = killmail['zkb']['totalValue']

        if character_name != "":
            self.kills.append(
                Kill(
                    kill_id,
                    character_id,
                    character_name,
                    ship_type_id,
                    solar_system_id,
                    date,
                    isk_destroyed
                )
            )