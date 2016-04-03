# generalstats.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import os
from skeleton import Skeleton
from statsconfig import StatsConfig
import csv
import numpy as np
import matplotlib.pyplot as plt
from calendar import monthrange


class GeneralStats(Skeleton):

    def __init__(self):
        self.json_file_name = "general_stats.json"
        self.pilot_set = set()
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

    def preprocess_output(self, dictionary):
        dictionary = super(self.__class__, self).preprocess_output(dictionary)
        del dictionary["security"]
        return dictionary

    def compute_avg_members(self):
        avg_members = 0

        date_start = (int(self.date_start.split('-')[0]), int(self.date_start.split('-')[1]))
        date_end = (int(self.date_end.split('-')[0]), int(self.date_end.split('-')[1]))

        if date_start == date_end:
            # same month
            (_, end_day) = monthrange(date_start[0], date_start[1])
            for corp_name in self.corp_names:
                avg_members += StatsConfig.member_count(
                    corp_name.replace(" ", "_"),
                    "{}-{:02d}-01".format(date_start[0], date_start[1]),
                    "{}-{:02d}-{}".format(date_start[0], date_start[1], end_day),
                )

        return avg_members

    def additional_processing(self, directory):
        # -------------------------------------------------
        sizes = np.array([
            self.total_kills_hs,
            self.total_kills_ls,
            self.total_kills_ns,
            self.total_kills_wh
        ])
        percentage = 100.*sizes/sizes.sum()
        labels = ['High-sec', 'Low-sec', 'Null-sec', 'W-space']
        labels2 = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labels, percentage)]
        colors = ['green', 'yellow', 'red', 'lightskyblue']

        plt.title("Total number of ships killed")
        patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels2, loc="best")
        plt.axis('equal')

        plt.plot()
        plt.savefig(os.path.join(directory, 'piechart_all_ships_destroyed'))

        # -------------------------------------------------
        sizes = np.array([
            self.total_value_hs,
            self.total_value_ls,
            self.total_value_ns,
            self.total_value_wh
        ])
        percentage = 100.*sizes/sizes.sum()
        labels = ['High-sec', 'Low-sec', 'Null-sec', 'W-space']
        labels2 = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labels, percentage)]
        colors = ['green', 'yellow', 'red', 'lightskyblue']

        plt.title("Total ISK destroyed")
        patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels2, loc="best")
        plt.axis('equal')

        plt.plot()
        plt.savefig(os.path.join(directory, 'piechart_all_isk_destroyed'))

    def process_km(self, killmail):
        self.total_kills += 1
        self.total_value += killmail['zkb']['totalValue']

        # activity
        for attacker in killmail['attackers']:
            # Wingspan attackers
            if attacker['corporationID'] in StatsConfig.CORP_IDS:
                self.pilot_set.add(attacker['characterID'])
                self.corp_names.add(attacker['corporationName'])

                date = killmail['killTime'].split()[0]
                if not self.date_start:
                    self.date_start = date
                    self.date_end = date
                if int(self.date_start.split('-')[2]) > int(date.split('-')[2]):
                    self.date_start = date
                if int(self.date_end.split('-')[2]) < int(date.split('-')[2]):
                    self.date_end = date

        [total_non_npc_attackers, wingspan_attackers] = StatsConfig.attacker_types(killmail)
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
