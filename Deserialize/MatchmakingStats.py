import json

class MatchmakingStats:
    def __init__(self, total_candidates=0, queue_type=None):
        self.total_candidates = total_candidates
        self.queue_type = queue_type

    def get_total_candidates(self):
        return self.total_candidates

    def set_total_candidates(self, total_candidates):
        self.total_candidates = total_candidates

    def get_queue_type(self):
        return self.queue_type

    def set_queue_type(self, queue_type):
        self.queue_type = queue_type

    @classmethod
    def from_json(cls, data):
        data_dict = json.loads(data)
        return cls(total_candidates=data_dict.get('totalCandidates', 0), queue_type=data_dict.get('queueType'))

