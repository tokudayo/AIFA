package com.google.mediapipe.apps.aifa.data;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class APIClient {

    private static Retrofit retrofit = null;

    public static Retrofit getClient() {
        retrofit = new Retrofit.Builder()
                .baseUrl("https://aifa.one/api/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();



        return retrofit;
    }

}