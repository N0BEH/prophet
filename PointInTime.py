import json
from datetime import timedelta, datetime

from MatchmakingStats import MatchmakingStats


class PointInTime:
    HOUR_TO_ADD = 2

    def __init__(self, total_candidates=0, total_servers=0 ,stats=None, time=None):
        if time is None:
            now = datetime.now()
            now = now + timedelta(hours=self.HOUR_TO_ADD)
            self.time = now.strftime("%d/%m/%Y %H:%M:%S.%f")
        else:
            self.time = time

        self.total_candidates = total_candidates
        self.total_servers = total_servers
        self.stats = stats if stats is not None else []

    def get_time(self):
        return self.time

    def get_total_candidates(self):
        return self.total_candidates

    def get_stats(self):
        return self.stats

    def get_total_servers(self):
        return self.total_servers

    @classmethod
    def from_json(cls, data):
        data_dict = json.loads(data)
        stats = [MatchmakingStats.from_json(json.dumps(stat)) for stat in data_dict.get('stats', [])]
        return cls(data_dict.get('totalCandidates', 0), data_dict.get('totalServers', 0), stats, data_dict.get('time'))

