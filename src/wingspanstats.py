# wingspanstats.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

import os
import json
import sys
from db_create import get_daterange

from rules.statsconfig import StatsConfig
from rules.agents import Agents
from rules.astero import Astero
from rules.awox import Awox
from rules.blops import Blops
from rules.bombers import Bombers
from rules.bombingrun import BombingRun
from rules.capitals import Capitals
from rules.explorerhunter import ExplorerHunter
from rules.generalstats import GeneralStats
from rules.industrygiant import IndustryGiant
from rules.interdictorace import InterdictorAce
from rules.minerbumper import MinerBumper
from rules.nestor import Nestor
from rules.podexpress import PodExpress
from rules.recons import Recons
from rules.ships import Ships
from rules.solohunter import SoloHunter
from rules.stratios import Stratios
from rules.t3cruiser import T3Cruiser
from rules.teamplayer import TeamPlayer
from rules.theracrusader import TheraCrusader
from rules.valuables import Valuables
from rules.victims import Victims


def defined_rules():
    return [
        Agents(),
        Astero(),
        Blops(),
        Bombers(),
        BombingRun(),
        Capitals(),
        ExplorerHunter(),
        GeneralStats(),
        IndustryGiant(),
        InterdictorAce(),
        MinerBumper(),
        Nestor(),
        PodExpress(),
        Recons(),
        Ships(),
        SoloHunter(),
        Stratios(),
        T3Cruiser(),
        TeamPlayer(),
        TheraCrusader(),
        Valuables(),
        Victims(),
    ]


def extract_killmails(file_name, rules_alltime, rules_monthly, awox_alltime, awox_monthly):
    with open(file_name) as data_file:
        data = json.load(data_file)

    for killmail in data:
        awox_alltime.process_km(killmail)
        awox_monthly.process_km(killmail)
        awox = False
        if killmail['victim']['corporationID'] in StatsConfig.CORP_IDS:
            awox = True

        [total_non_npc_attackers, wingspan_attackers] = StatsConfig.attacker_types(killmail)
        if total_non_npc_attackers > 0:
            if not awox or StatsConfig.INCLUDE_AWOX:
                if float(wingspan_attackers) / float(total_non_npc_attackers) >= StatsConfig.FLEET_COMP:
                    for rule in rules_alltime:
                        rule.process_km(killmail)
                    for rule in rules_monthly:
                        rule.process_km(killmail)


def analyze_data(db_list):
    rules_alltime = defined_rules()
    awox_alltime = Awox()

    for (year, month) in db_list:
        db_dir = os.path.join(StatsConfig.DATABASE_PATH, "{}-{:02d}".format(year, month))

        if os.path.exists(db_dir):
            rules_monthly = defined_rules()
            awox_monthly = Awox()
            print "Analyzing", db_dir

            page_nr = 1
            while True:
                file_name = os.path.join(db_dir, "{}-{:02d}_{:02d}.json".format(year, month, page_nr))

                if os.path.exists(file_name):
                    extract_killmails(file_name, rules_alltime, rules_monthly, awox_alltime, awox_monthly)
                    page_nr += 1
                else:
                    break

            for rule in rules_monthly:
                rule.output_results(os.path.join(StatsConfig.RESULTS_PATH, "{}-{:02d}".format(year, month)))
            awox_monthly.output_results(os.path.join(StatsConfig.RESULTS_PATH, "{}-{:02d}".format(year, month)))

    for rule in rules_alltime:
        rule.output_results(os.path.join(StatsConfig.RESULTS_PATH, '__alltime__'))
    awox_alltime.output_results(os.path.join(StatsConfig.RESULTS_PATH, '__alltime__'))


def main():
    args = sys.argv

    daterange = get_daterange(args[1] if len(args) >= 2 else None, args[2] if len(args) >= 3 else None)
    if not daterange:
        print "You have to specify the start date and optionally the end date in format YYYY-MM"
        return

    analyze_data(map(lambda x: (x['year'], x['month']), daterange))

if __name__ == "__main__":
    main()
