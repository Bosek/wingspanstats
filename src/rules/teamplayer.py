# teamplayer.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class TeamPlayer(Skeleton):

    def __init__(self):
        self.json_file_name = "team_player.json"
        self.agent_ships_destroyed = list()
        self.agent_isk_destroyed = list()

    def sort(self):
        self.agent_ships_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)
        self.agent_isk_destroyed.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        isk_destroyed = killmail['zkb']['totalValue']

        [_, wingspan_attackers] = StatsConfig.attacker_types(killmail)
        if wingspan_attackers > 1:
            # fleet kill

            for attacker in killmail['attackers']:
                if attacker['corporationID'] in StatsConfig.CORP_IDS:
                    attacker_name = attacker['characterName']

                    if attacker_name != "":
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
