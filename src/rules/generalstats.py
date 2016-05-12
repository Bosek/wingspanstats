# generalstats.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import os
from skeleton import Skeleton
from statsconfig import StatsConfig
import csv
import numpy as np
from calendar import monthrange
from datetime import datetime


class GeneralStats(Skeleton):

    def __init__(self):
        self.json_file_name = "general_stats.json"
        self.pilots = set()
        self.total_kills = 0
        self.total_value = 0
        self.solo_total_kills = 0
        self.solo_total_value = 0

        self.total_kills_hs = 0
        self.total_value_hs = 0
        self.total_kills_ls = 0
        self.total_value_ls = 0
        self.total_kills_ns = 0
        self.total_value_ns = 0
        self.total_kills_wh = 0
        self.total_value_wh = 0

        self.wh_stats = list()
        self.corp_names = set([])
        self.date_start = None
        self.date_end = None

        with open('security.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.security = {int(rows[0]): rows[1] for rows in reader}

    def preprocess_output(self):
        dictionary = super(self.__class__, self).preprocess_output()
        del dictionary["security"]
        del dictionary["pilots"]
        return dictionary

    def process_km(self, killmail):
        self.total_kills += 1
        self.total_value += killmail['zkb']['totalValue']

        # activity
        for attacker in killmail['attackers']:
            # Wingspan attackers
            if attacker['corporationID'] in StatsConfig.CORP_IDS:
                self.pilots.add(attacker['characterID'])
                self.corp_names.add(attacker['corporationName'])

                date = killmail['killTime'].split()[0]
                if not self.date_start:
                    self.date_start = date
                    self.date_end = date
                newdate = map(lambda x: int(x), date.split('-'))
                newdate = datetime(newdate[0], newdate[1], newdate[2])
                olddate_start = map(lambda x: int(x), self.date_start.split('-'))
                olddate_start = datetime(olddate_start[0], olddate_start[1], olddate_start[2])
                olddate_end = map(lambda x: int(x), self.date_end.split('-'))
                olddate_end = datetime(olddate_end[0], olddate_end[1], olddate_end[2])

                if newdate < olddate_start:
                    self.date_start = date
                if newdate > olddate_end:
                    self.date_end = date

        [total_non_npc_attackers,
            wingspan_attackers] = StatsConfig.attacker_types(killmail)
        if total_non_npc_attackers == wingspan_attackers and wingspan_attackers == 1:
            self.solo_total_kills += 1
            self.solo_total_value += killmail['zkb']['totalValue']

        system_id = killmail['solarSystemID']
        if self.security[system_id] == "hs":  # high-sec
            self.total_kills_hs += 1
            self.total_value_hs += killmail['zkb']['totalValue']
        elif self.security[system_id] == "ls":  # low-sec
            self.total_kills_ls += 1
            self.total_value_ls += killmail['zkb']['totalValue']
        elif self.security[system_id] == "ns":  # null-sec
            self.total_kills_ns += 1
            self.total_value_ns += killmail['zkb']['totalValue']
        else:  # w-space
            self.total_kills_wh += 1
            self.total_value_wh += killmail['zkb']['totalValue']

            wh_stats = filter(
                lambda x: x.get('type') == self.security[system_id],
                self.wh_stats
            )

            # stats for each wh class
            if len(wh_stats):
                wh_index = self.wh_stats.index(wh_stats[0])
                self.wh_stats[wh_index]['destroyed'] += 1
                self.wh_stats[wh_index]['total_value'] += killmail['zkb']['totalValue']
            else:
                self.wh_stats.append({
                    'type': self.security[system_id],
                    'destroyed': 1,
                    'total_value': killmail['zkb']['totalValue']
                })
