package org.example;

import org.example.queueTypes.QueueType;

public class MatchmakingStats {

    private int totalCandidates;
    private QueueType queueType;

    public MatchmakingStats() {

    }

    public MatchmakingStats(QueueType queueType) {
        this.queueType = queueType;
    }

    public MatchmakingStats(int totalCandidates, QueueType queueType) {
        this.totalCandidates = totalCandidates;
        this.queueType = queueType;
    }

    public int getTotalCandidates() {
        return totalCandidates;
    }

    public void setTotalCandidates(int totalCandidates) {
        this.totalCandidates = totalCandidates;
    }

    public QueueType getQueueType() {
        return queueType;
    }

    public void setQueueType(QueueType queueType) {
        this.queueType = queueType;
    }

}
