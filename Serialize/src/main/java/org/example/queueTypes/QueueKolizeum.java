package org.example.queueTypes;

public class QueueKolizeum extends QueueType {

    public QueueKolizeum(int perPlayerTeam, int maxTeams) {
        super(perPlayerTeam, maxTeams);
    }

    public QueueKolizeum(int perPlayerTeam, int priority, String serverName, int maxTeams) {
        super(perPlayerTeam, priority, serverName, maxTeams);
    }

    public String getLoreDisplay() {
        return "kolizeum_display_lore";
    }

    @Override
    public String getStatusDescription() {
        return "kolizeum_status_description";
    }

    @Override
    public String getTypeDisplay() {
        return " " + this.perPlayerTeam + "Vs" + this.perPlayerTeam;
    }

    public String getMaterial() {
        return "NETHERITE_SWORD";
    }

    public QueueKolizeum() {
        super();
    }

    public QueueKolizeum(boolean action) {
        super();
    }

    public String getDisplayName() {
        return "kolizeum_display_name";
    }

    @Override
    public String getColor() {
        return "&6";
    }

    @Override
    public String toString() {
        return "KOLIZEUM";
    }

    @Override
    public boolean equals(QueueType type) {
        return type instanceof QueueKolizeum && this.getPerPlayerTeam() == type.getPerPlayerTeam();
    }

    @Override
    public boolean isTypeOf(QueueType type) {
        return type instanceof QueueKolizeum;
    }
}
