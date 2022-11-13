package com.google.mediapipe.apps.aifa.ui.signup;

import androidx.annotation.Nullable;

/**
 * Authentication result : success (user details) or error message.
 */
class SignupResult {
    @Nullable
    private SignedUpUserView success;
    @Nullable
    private Integer error;

    SignupResult(@Nullable Integer error) {
        this.error = error;
    }

    SignupResult(@Nullable SignedUpUserView success) {
        this.success = success;
    }

    @Nullable
    SignedUpUserView getSuccess() {
        return success;
    }

    @Nullable
    Integer getError() {
        return error;
    }
}