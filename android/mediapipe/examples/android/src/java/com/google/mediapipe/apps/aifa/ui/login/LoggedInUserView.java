package com.google.mediapipe.apps.aifa.ui.login;

/**
 * Class exposing authenticated user details to the UI.
 */
class LoggedInUserView {
    private String displayName;
    private Integer userId;
    private String accessToken;
    //... other data fields that may be accessible to the UI

    LoggedInUserView(String displayName, Integer userId, String accessToken) {
        this.displayName = displayName;
        this.userId = userId;
        this.accessToken = accessToken;
    }

    String getDisplayName() {
        return displayName;
    }

    Integer getUserId() {
        return userId;
    }

    String getAccessToken() {
        return accessToken;
    }
}