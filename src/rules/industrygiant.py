# industrygiant.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.agent import Agent


class IndustryGiant(Skeleton):

    def __init__(self):
        self.json_file_name = "industry_giant.json"
        self.agents = list()

    def sort(self):
        self.agents.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

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
                attacker_id = attacker['characterID']
                attacker_name = attacker['characterName']
                attacker_corp = attacker['corporationID']

                if attacker_name != "" and attacker_corp in StatsConfig.CORP_IDS:
                    agents = filter(
                        lambda x: x.character_name == attacker_name,
                        self.agents
                    )

                    if len(agents):
                        agent_index = self.agents.index(agents[0])
                        self.agents[agent_index].ships_destroyed += 1
                        self.agents[agent_index].isk_destroyed += isk_destroyed
                    else:
                        self.agents.append(
                            Agent(attacker_id, attacker_name, 1, isk_destroyed)
                        )
