# interdictorace.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class InterdictorAce(Skeleton):

    def __init__(self):
        self.json_file_name = "interdictor_ace.json"
        self.agent_ships_destroyed = list()
        self.agent_isk_destroyed = list()

    def sort(self):
        self.agent_ships_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)
        self.agent_isk_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        for attacker in killmail['attackers']:
            attacker_name = attacker['characterName']
            attacker_corp = attacker['corporationID']
            attacker_ship = attacker['shipTypeID']

            if attacker_name != "" and attacker_corp in StatsConfig.CORP_IDS:
                if attacker_ship in [
                    22460, 22464, 22452, 22456,  # interdictors
                    12013, 12017, 11995, 12021,  # heavy interdictors
                ]:
                    agent_ships_destroyed = filter(
                        lambda x: x.get('name') == attacker_name,
                        self.agent_ships_destroyed
                    )
                    agent_isk_destroyed = filter(
                        lambda x: x.get('name') == attacker_name,
                        self.agent_isk_destroyed
                    )

                    if len(agent_ships_destroyed):
                        agent_index = self.agent_ships_destroyed.index(agent_ships_destroyed[0])
                        self.agent_ships_destroyed[agent_index]['destroyed'] += 1
                    else:
                        self.agent_ships_destroyed.append({'name': attacker_name, 'destroyed': 1})

                    if len(agent_isk_destroyed):
                        agent_index = self.agent_isk_destroyed.index(agent_isk_destroyed[0])
                        self.agent_isk_destroyed[agent_index]['destroyed'] += isk_destroyed
                    else:
                        self.agent_isk_destroyed.append({'name': attacker_name, 'destroyed': isk_destroyed})
