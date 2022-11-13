
package com.google.mediapipe.apps.aifa.data.pojo;


import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SignUpResponse {

    @SerializedName("email")
    @Expose
    public String email;
    @SerializedName("password")
    @Expose
    public String password;
    @SerializedName("refreshToken")
    @Expose
    public Object refreshToken;
    @SerializedName("id")
    @Expose
    public Integer id;
    @SerializedName("createdAt")
    @Expose
    public String createdAt;
    @SerializedName("updatedAt")
    @Expose
    public String updatedAt;

}