package org.example;

import org.example.MatchmakingStats;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

public class PointInTime {

    private final int hourtoadd = 2;
    private String time;
    private int totalCandidates;

    private int totalServers;
    private List<MatchmakingStats> stats;

    public PointInTime() {
    }

    public PointInTime(int totalCandidates, int totalServers, List<MatchmakingStats> stats) {

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss.SS");
        LocalDateTime now = LocalDateTime.now();

        this.time = now.format(formatter);
        this.totalCandidates = totalCandidates;
        this.stats = stats;
        this.totalServers = totalServers;
    }

    public PointInTime(String time, int totalCandidates, List<MatchmakingStats> stats) {
        this.time = time;
        this.totalCandidates = totalCandidates;
        this.stats = stats;
    }

    public String getTime() {
        return this.time;
    }

    public int getTotalCandidates() {
        return this.totalCandidates;
    }

    public List<MatchmakingStats> getStats() {
        return this.stats;
    }

}
