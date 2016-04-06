# mostvalueable.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class MostValuable(Skeleton):

    def __init__(self):
        self.json_file_name = "most_valuable.json"
        self.most_valuable = list()

    def sort(self):
        self.most_valuable.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        kill_id = killmail['killID']
        isk_destroyed = killmail['zkb']['totalValue']
        self.most_valuable.append({'kill_id': kill_id, 'destroyed': isk_destroyed})


class MostValuableSolo(Skeleton):

    def __init__(self):
        self.json_file_name = "most_valuable_solo.json"
        self.most_valuable = list()

    def sort(self):
        self.most_valuable.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        kill_id = killmail['killID']
        isk_destroyed = killmail['zkb']['totalValue']

        [total_non_npc_attackers, wingspan_attackers] = StatsConfig.attacker_types(killmail)
        if total_non_npc_attackers == wingspan_attackers and wingspan_attackers == 1:
            # solo kill
            attacker_name = ""
            for attacker in killmail['attackers']:
                if attacker['corporationID'] in StatsConfig.CORP_IDS:
                    attacker_name = attacker['characterName']
                    break

            self.most_valuable.append({
                'kill_id': kill_id,
                'name': attacker_name,
                'destroyed': isk_destroyed
            })
