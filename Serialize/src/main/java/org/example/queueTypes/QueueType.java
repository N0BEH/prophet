package org.example.queueTypes;

public abstract class QueueType {
    protected int perPlayerTeam;
    private int priority;
    private String serverName;

    protected int maxTeams;

    public QueueType() {

    }

    public QueueType(int perPlayerTeam, int maxTeams) {
        this.perPlayerTeam = perPlayerTeam;
        this.maxTeams = maxTeams;
        this.priority = 0;

        this.serverName = this.toString().toLowerCase();
    }

    public QueueType(int perPlayerTeam, int priority, String serverName, int maxTeams) {
        this.perPlayerTeam = perPlayerTeam;
        this.priority = priority;
        this.serverName = serverName;
        this.maxTeams = maxTeams;
    }

    public abstract String getLoreDisplay();

    public abstract String getTypeDisplay();

    public abstract String getMaterial();

    public abstract String getDisplayName();

    public abstract String getColor();

    public abstract String getStatusDescription();

    public int getPriority() {
        return priority;
    }

    public int getMaxTeams() {
        return maxTeams;
    }

    public String getServerName() {
        return serverName;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }

    public int getPerPlayerTeam() {
        return perPlayerTeam;
    }

    public void setPerPlayerTeam(int perPlayerTeam) {
        this.perPlayerTeam = perPlayerTeam;
    }

    public abstract String toString();

    public abstract boolean equals(QueueType type);

    public abstract boolean isTypeOf(QueueType type);

}
