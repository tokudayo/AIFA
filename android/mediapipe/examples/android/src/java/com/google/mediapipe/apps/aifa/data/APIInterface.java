package com.google.mediapipe.apps.aifa.data;

import com.google.mediapipe.apps.aifa.data.pojo.AuthRequest;
import com.google.mediapipe.apps.aifa.data.pojo.AuthResponse;
import com.google.mediapipe.apps.aifa.data.pojo.SignUpRequest;
import com.google.mediapipe.apps.aifa.data.pojo.SignUpResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface APIInterface {

    @POST("auth/login")
    Call<AuthResponse> login(@Body AuthRequest user);

    @POST("auth/sign-up")
    Call<SignUpResponse> signup(@Body SignUpRequest user);
}