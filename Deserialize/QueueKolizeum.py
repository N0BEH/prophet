from QueueType import QueueType


class QueueKolizeum(QueueType):
    def __init__(self, per_player_team=0, max_teams=0, priority=0, server_name=None, action=False):
        super().__init__(per_player_team, max_teams, priority, server_name)

    def get_lore_display(self):
        return "kolizeum_display_lore"

    def get_status_description(self):
        return "kolizeum_status_description"

    def get_type_display(self):
        return f" {self.per_player_team}Vs{self.per_player_team}"

    def get_material(self):
        return "NETHERITE_SWORD"

    def get_display_name(self):
        return "kolizeum_display_name"

    def get_color(self):
        return "&6"

    def __str__(self):
        return "KOLIZEUM"

    def __eq__(self, other):
        return isinstance(other, QueueKolizeum) and self.get_per_player_team() == other.get_per_player_team()

    def is_type_of(self, other):
        return isinstance(other, QueueKolizeum)