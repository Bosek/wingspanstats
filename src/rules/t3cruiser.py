# t3cruiser.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.agent import Agent


class T3Cruiser(Skeleton):

    def __init__(self):
        self.json_file_name = "t3cruiser.json"
        self.agents = list()

    def sort(self):
        self.agents.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        for attacker in killmail['attackers']:
            attacker_id = attacker['characterID']
            attacker_name = attacker['characterName']
            attacker_corp = attacker['corporationID']
            attacker_ship = attacker['shipTypeID']

            if attacker_name != "" and attacker_corp in StatsConfig.CORP_IDS:
                if attacker_ship in [29986, 29990, 29988, 29984]:
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
