import json

from QueueType import QueueType


class QueueQuest(QueueType):
    def __init__(self, per_player_team=0, max_teams=0, priority=0, server_name=None, action=False):
        super().__init__(per_player_team, max_teams, priority, server_name)

    def get_lore_display(self):
        return "quest_display_lore"

    def get_status_description(self):
        return "quest_status_description"

    def get_type_display(self):
        return f" {self.per_player_team} joueurs"

    def get_material(self):
        return "WRITTEN_BOOK"

    def get_display_name(self):
        return "quest_display_name"

    def get_color(self):
        return "&6"

    def __str__(self):
        return "QUEST"

    def __eq__(self, other):
        return isinstance(other, QueueQuest) and self.get_per_player_team() == other.get_per_player_team()

    def is_type_of(self, other):
        return isinstance(other, QueueQuest)

    @classmethod
    def from_json(cls, data):
        data_dict = json.loads(data)
        return cls(data_dict.get('perPlayerTeam', 0), data_dict.get('maxTeams', 0), data_dict.get('priority', 0),
                   data_dict.get('serverName'), data_dict.get('action', False))