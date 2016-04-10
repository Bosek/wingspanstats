# solohunter.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.agent import Agent


class SoloHunter(Skeleton):

    def __init__(self):
        self.json_file_name = "solo_hunter.json"
        self.agents = list()

    def sort(self):
        self.agents.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        [
            total_non_npc_attackers,
            wingspan_attackers
        ] = StatsConfig.attacker_types(killmail)
        if total_non_npc_attackers == wingspan_attackers and wingspan_attackers == 1:
            # solo kill
            attacker_id = ""
            attacker_name = ""
            for attacker in killmail['attackers']:
                if attacker['corporationID'] in StatsConfig.CORP_IDS:
                    attacker_id = attacker['characterID']
                    attacker_name = attacker['characterName']
                    break

            if attacker_name != "":
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
