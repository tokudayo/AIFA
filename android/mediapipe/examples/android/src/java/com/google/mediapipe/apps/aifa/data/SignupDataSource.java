package com.google.mediapipe.apps.aifa.data;

import com.google.mediapipe.apps.aifa.data.model.SignedUpUser;

import java.io.IOException;

/**
 * Class that handles authentication w/ signup credentials and retrieves user information.
 */
public class SignupDataSource {

    public Result<SignedUpUser> signup(String username, String password) {

        try {
            // TODO: handle signedUpUser authentication
            SignedUpUser fakeUser =
                    new SignedUpUser(
                            java.util.UUID.randomUUID().toString(),
                            "Jane Doe");
            return new Result.Success<>(fakeUser);
        } catch (Exception e) {
            return new Result.Error(new IOException("Error signing up", e));
        }
    }

    public void logout() {
        // TODO: revoke authentication
    }
}