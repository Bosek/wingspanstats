# industrygiant.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class IndustryGiant(Skeleton):

    def __init__(self):
        self.json_file_name = "industry_giant.json"
        self.agent_ships_destroyed = list()
        self.agent_isk_destroyed = list()

    def sort(self):
        self.agent_ships_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)
        self.agent_isk_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        if killmail['victim']['shipTypeID'] in [
            648, 1944, 33695, 655, 651, 33689, 657, 654,  # industrials
            652, 33693, 656, 32811, 4363, 4388, 650, 2998,  # industrials
            2863, 19744, 649, 33691, 653,  # industrials
            12729, 12733, 12735, 12743,  # blockade runners
            12731, 12753, 12747, 12745,  # deep space transports
            34328, 20185, 20189, 20187, 20183,  # freighters
            28848, 28850, 28846, 28844,  # jump freighters
            28606, 33685, 28352, 33687,  # orca, rorqual
        ]:
            isk_destroyed = killmail['zkb']['totalValue']

            for attacker in killmail['attackers']:
                attacker_name = attacker['characterName']
                attacker_corp = attacker['corporationID']

                if attacker_name != "" and attacker_corp in StatsConfig.CORP_IDS:
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
