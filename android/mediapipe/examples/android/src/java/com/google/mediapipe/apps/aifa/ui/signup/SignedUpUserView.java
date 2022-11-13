package com.google.mediapipe.apps.aifa.ui.signup;

/**
 * Class exposing authenticated user details to the UI.
 */
class SignedUpUserView {
    private String displayName;
    //... other data fields that may be accessible to the UI

    SignedUpUserView(String displayName) {
        this.displayName = displayName;
    }

    String getDisplayName() {
        return displayName;
    }
}