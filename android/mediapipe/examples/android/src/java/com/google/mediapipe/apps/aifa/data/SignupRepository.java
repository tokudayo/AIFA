package com.google.mediapipe.apps.aifa.data;

import com.google.mediapipe.apps.aifa.data.model.SignedUpUser;

/**
 * Class that requests authentication and user information from the remote data source and
 * maintains an in-memory cache of signup status and user credentials information.
 */
public class SignupRepository {

    private static volatile SignupRepository instance;

    private SignupDataSource dataSource;

    // If user credentials will be cached in local storage, it is recommended it be encrypted
    // @see https://developer.android.com/training/articles/keystore
    private SignedUpUser user = null;

    // private constructor : singleton access
    private SignupRepository(SignupDataSource dataSource) {
        this.dataSource = dataSource;
    }

    public static SignupRepository getInstance(SignupDataSource dataSource) {
        if (instance == null) {
            instance = new SignupRepository(dataSource);
        }
        return instance;
    }

    public boolean isSignedUp() {
        return user != null;
    }

    public void logout() {
        user = null;
        dataSource.logout();
    }

    private void setSignedUpUser(SignedUpUser user) {
        this.user = user;
        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
    }

    public Result<SignedUpUser> signup(String username, String password) {
        // handle signup
        Result<SignedUpUser> result = dataSource.signup(username, password);
        if (result instanceof Result.Success) {
            setSignedUpUser(((Result.Success<SignedUpUser>) result).getData());
        }
        return result;
    }
}