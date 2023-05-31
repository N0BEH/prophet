package org.example;

import com.google.gson.Gson;
import org.example.queueTypes.QueueKolizeum;
import redis.clients.jedis.HostAndPort;
import redis.clients.jedis.Jedis;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

public class Main {

    private static double toRadians(double secondsSinceMidnight) {
        return Math.PI * secondsSinceMidnight / (12 * 60 * 60);
    }

    public static void main(String[] args) {

        // Créer une nouvelle instance de Jedis
        HostAndPort jedisConnexion = new HostAndPort("localhost", 6380);
        Jedis jedis = new Jedis(jedisConnexion);

        System.out.println("Connexion à Redis réussie : " + jedis.ping());

        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now;

        //Destroy all data in redis
        //jedis.flushAll();

        int totalPeriods = 15 * 24 * 60 / 5;

        for (int i = 0; i < totalPeriods; i++) {
            String key = startTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd/HH-mm-ss"));

            long secondsSinceMidnight = ChronoUnit.SECONDS.between(startTime.toLocalDate().atStartOfDay(), startTime);
            double radians = toRadians(secondsSinceMidnight);

            int value = (int) Math.ceil((Math.sin(radians) + 1) / 2 * 12);
            int value2 = (int) Math.ceil((Math.sin(radians) + 1) / 2 * 8);

            //jedis.set("Elypool:PointInTime:" + key + ":servers", String.valueOf(value));
            //jedis.set("Elypool:PointInTime:" + key + ":candidates", String.valueOf(value2));

            List<MatchmakingStats> matchs = new ArrayList<>();
            matchs.add(new MatchmakingStats(value, new QueueKolizeum(1,2)));
            matchs.add(new MatchmakingStats(0, new QueueKolizeum(2,2)));
            matchs.add(new MatchmakingStats(0, new QueueKolizeum(3,2)));
            PointInTime pointInTime = new PointInTime(value, value2, matchs);

            Gson gson = new Gson();
            String pointInTimeJson = gson.toJson(pointInTime);
            jedis.set("ElyPool:Statistics:PointsInTime:" + key, pointInTimeJson);

            startTime = startTime.minusMinutes(5);
        }


    }
}