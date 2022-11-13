package com.google.mediapipe.apps.aifa.data.pojo;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class AuthResponse {

    @SerializedName("accessToken")
    @Expose
    public String accessToken;
    @SerializedName("refreshToken")
    @Expose
    public String refreshToken;
    @SerializedName("user")
    @Expose
    public User user;

}