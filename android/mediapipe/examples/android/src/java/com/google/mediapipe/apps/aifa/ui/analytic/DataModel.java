package com.google.mediapipe.apps.aifa.ui.analytic;

public class DataModel {
    String exercise;
    String platform;
    String correct;
    String startTime;
    String endTime;

    public DataModel(String exercise,
                     String platform,
                     String correct,
                     String startTime,
                     String endTime) {
        this.exercise = exercise;
        this.platform = platform;
        this.correct = correct;
        this.startTime = startTime;
        this.endTime = endTime;
    }

    public String getCorrect() {
        return correct;
    }

    public String getExercise() {
        return exercise;
    }

    public String getEndTime() {
        return endTime;
    }

    public String getPlatform() {
        return platform;
    }

    public String getStartTime() {
        return startTime;
    }
}
