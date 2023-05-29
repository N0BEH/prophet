package org.example.queueTypes;

public class QueueQuest extends QueueType {
    public QueueQuest(int perPlayerTeam, int maxTeams) {
        super(perPlayerTeam, maxTeams);
    }

    public QueueQuest(int perPlayerTeam, int priority, String serverName, int maxTeams) {
        super(perPlayerTeam, priority, serverName, maxTeams);
    }

    public String getLoreDisplay() {
        return "quest_display_lore";
    }

    @Override
    public String getTypeDisplay() {
        return this.perPlayerTeam + " joueurs";
    }

    public String getMaterial() {
        return "WRITTEN_BOOK";
    }

    public QueueQuest() {
        super();
    }

    public QueueQuest(boolean action) {
        super();
    }

    public String getDisplayName() {
        return "quest_display_name";
    }

    @Override
    public String getColor() {
        return "&3";
    }

    @Override
    public String getStatusDescription() {
        return "quest_status_description";
    }

    @Override
    public String toString() {
        return "QUEST";
    }

    @Override
    public boolean equals(QueueType type) {
        return type instanceof QueueQuest && this.getPerPlayerTeam() == type.getPerPlayerTeam();
    }

    @Override
    public boolean isTypeOf(QueueType type) {
        return type instanceof QueueQuest;
    }
}
