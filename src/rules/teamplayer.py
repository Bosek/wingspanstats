# teamplayer.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig
from models.agent import Agent


class TeamPlayer(Skeleton):

    def __init__(self):
        self.json_file_name = "team_player.json"
        self.agents = list()

    def sort(self):
        self.agents.sort(key=lambda x: x.isk_destroyed * x.ships_destroyed, reverse=True)

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        [_, wingspan_attackers] = StatsConfig.attacker_types(killmail)
        if wingspan_attackers > 1:
            # fleet kill

            for attacker in killmail['attackers']:
                if attacker['corporationID'] in StatsConfig.CORP_IDS:
                    attacker_id = attacker['characterID']
                    attacker_name = attacker['characterName']

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
