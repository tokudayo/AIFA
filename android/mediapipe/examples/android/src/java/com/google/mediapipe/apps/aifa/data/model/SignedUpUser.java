package com.google.mediapipe.apps.aifa.data.model;

/**
 * Data class that captures user information for logged in users retrieved from LoginRepository
 */
public class SignedUpUser {

    private String userId;
    private String displayName;

    public SignedUpUser(String userId, String displayName) {
        this.userId = userId;
        this.displayName = displayName;
    }

    public String getUserId() {
        return userId;
    }

    public String getDisplayName() {
        return displayName;
    }
}