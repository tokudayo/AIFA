package com.google.mediapipe.apps.aifa.data.pojo;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Analytic {
    @SerializedName("id")
    @Expose
    public Integer id;
    @SerializedName("startTime")
    @Expose
    public String startTime;
    @SerializedName("endTime")
    @Expose
    public String endTime;
    @SerializedName("exercise")
    @Expose
    public String exercise;
    @SerializedName("platform")
    @Expose
    public String platform;
    @SerializedName("correct")
    @Expose
    public String correct;
    @SerializedName("createdAt")
    @Expose
    public String createdAt;
    @SerializedName("updatedAt")
    @Expose
    public String updatedAt;

}