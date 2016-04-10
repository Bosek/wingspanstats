# explorerhunter.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.agent import Agent


class ExplorerHunter(Skeleton):

    def __init__(self):
        self.json_file_name = "explorer_hunter.json"
        self.agents = list()

    def sort(self):
        self.agents.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

    def process_km(self, killmail):
        victim_is_explorer = False
        for item in killmail['items']:
            # midslots
            if item['flag'] >= 19 and item['flag'] <= 26:
                # relic and data analyzers
                if item['typeID'] in [22177, 30832, 22175, 30834, 3581]:
                    victim_is_explorer = True
                    break

        if victim_is_explorer:
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
