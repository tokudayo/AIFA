package com.google.mediapipe.apps.aifa.data.pojo;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class User {
    @SerializedName("id")
    @Expose
    public Integer id;
    @SerializedName("email")
    @Expose
    public String email;
    @SerializedName("accessToken")
    @Expose
    public String accessToken;
    @SerializedName("refreshToken")
    @Expose
    public String refreshToken;
    @SerializedName("password")
    @Expose
    public String password;
    @SerializedName("createdAt")
    @Expose
    public String createdAt;
    @SerializedName("updatedAt")
    @Expose
    public String updatedAt;

}