from datetime import datetime, timedelta

class PointInTime:
    HOUR_TO_ADD = 2

    def __init__(self, total_candidates=0, stats=None, time=None):
        if time is None:
            now = datetime.now()
            now = now + timedelta(hours=self.HOUR_TO_ADD)
            self.time = now.strftime("%d/%m/%Y %H:%M:%S.%f")
        else:
            self.time = time

        self.total_candidates = total_candidates
        self.stats = stats if stats is not None else []

    def get_time(self):
        return self.time

    def get_total_candidates(self):
        return self.total_candidates

    def get_stats(self):
        return self.stats