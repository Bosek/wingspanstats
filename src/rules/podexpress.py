# podexpress.py
# Author: Valtyr Farshield
# Author: Tomas Bosek

from skeleton import Skeleton
from statsconfig import StatsConfig


class PodExpress(Skeleton):

    def __init__(self):
        self.json_file_name = "pod_express.json"
        self.most_valuable = list()

    def sort(self):
        self.most_valuable.sort(key=lambda x: x['destroyed'], reverse=True)

    def process_km(self, killmail):
        if killmail['victim']['shipTypeID'] in [670, 33328]:
            kill_id = killmail['killID']
            isk_destroyed = killmail['zkb']['totalValue']
            self.most_valuable.append({'kill_id': kill_id, 'destroyed': isk_destroyed})
