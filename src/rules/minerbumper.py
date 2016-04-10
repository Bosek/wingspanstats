# minerbumper.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.agent import Agent


class MinerBumper(Skeleton):

    def __init__(self):
        self.json_file_name = "miner_bumper.json"
        self.agents = list()

    def sort(self):
        self.agents.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

    def process_km(self, killmail):
        if killmail['victim']['shipTypeID'] in [
            32880, 33697, 37135,  # mining frigates
            17476, 17480, 17478,  # mining barges
            22544, 22548, 33683, 22546  # exhumers
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
