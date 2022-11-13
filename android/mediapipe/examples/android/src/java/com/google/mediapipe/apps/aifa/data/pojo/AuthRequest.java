package com.google.mediapipe.apps.aifa.data.pojo;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class AuthRequest {
    @SerializedName("username")
    @Expose
    public String username;
    @SerializedName("password")
    @Expose
    public String password;

    public AuthRequest(String username, String password) {
        this.username = username;
        this.password = password;
    }
}