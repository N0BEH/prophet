from abc import ABC, abstractmethod

class QueueType(ABC):
    def __init__(self, per_player_team=0, max_teams=0, priority=0, server_name=None):
        self.per_player_team = per_player_team
        self.max_teams = max_teams
        self.priority = priority
        self.server_name = server_name if server_name else str(self).lower()
        self.action = None  # Placeholder for IActivityManager.InventoryAction

    @abstractmethod
    def get_lore_display(self):
        pass

    @abstractmethod
    def get_type_display(self):
        pass

    @abstractmethod
    def get_material(self):
        pass

    @abstractmethod
    def get_display_name(self):
        pass

    @abstractmethod
    def get_color(self):
        pass

    @abstractmethod
    def get_status_description(self):
        pass

    def get_priority(self):
        return self.priority

    def get_max_teams(self):
        return self.max_teams

    def get_action(self):
        return self.action

    def get_server_name(self):
        return self.server_name

    def set_priority(self, priority):
        self.priority = priority

    def set_action(self, action):
        self.action = action

    def get_per_player_team(self):
        return self.per_player_team

    def set_per_player_team(self, per_player_team):
        self.per_player_team = per_player_team

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def is_type_of(self, other):
        pass