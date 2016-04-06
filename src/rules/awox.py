# awox.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class Awox(Skeleton):

    def __init__(self):
        self.json_file_name = "top_awox.json"
        self.awox_kills = list()

    def sort(self):
        self.awox_kills.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        if killmail['victim']['corporationID'] in StatsConfig.CORP_IDS:
            kill_id = killmail['killID']
            isk_destroyed = killmail['zkb']['totalValue']
            victim_name = killmail['victim']['characterName']

            self.awox_kills.append({
                'kill_id': kill_id,
                'victim_name': victim_name,
                'destroyed': isk_destroyed
            })
