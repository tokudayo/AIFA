package com.google.mediapipe.apps.aifa.ui.login;

/**
 * Class exposing authenticated user details to the UI.
 */
class LoggedInUserView {
    private String displayName;
    private Integer userId;
    //... other data fields that may be accessible to the UI

    LoggedInUserView(String displayName, Integer userId) {
        this.displayName = displayName;
        this.userId = userId;
    }

    String getDisplayName() {
        return displayName;
    }

    Integer getUserId() {
        return userId;
    }
}