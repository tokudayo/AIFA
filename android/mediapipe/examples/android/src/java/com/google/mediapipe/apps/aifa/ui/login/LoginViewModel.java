package com.google.mediapipe.apps.aifa.ui.login;

import android.util.Patterns;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.google.mediapipe.apps.aifa.R;
import com.google.mediapipe.apps.aifa.data.APIInterface;
import com.google.mediapipe.apps.aifa.data.LoginRepository;
import com.google.mediapipe.apps.aifa.data.pojo.AuthRequest;
import com.google.mediapipe.apps.aifa.data.pojo.AuthResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginViewModel extends ViewModel {

    private MutableLiveData<LoginFormState> loginFormState = new MutableLiveData<>();
    private MutableLiveData<LoginResult> loginResult = new MutableLiveData<>();
    private LoginRepository loginRepository;

    LoginViewModel(LoginRepository loginRepository) {
        this.loginRepository = loginRepository;
    }

    LiveData<LoginFormState> getLoginFormState() {
        return loginFormState;
    }

    LiveData<LoginResult> getLoginResult() {
        return loginResult;
    }

    public void login(APIInterface apiInterface, String username, String password) {
        // can be launched in a separate asynchronous job
        /**
         Create new user
         **/
        AuthRequest authRequest = new AuthRequest(username, password);
        Call<AuthResponse> call = apiInterface.login(authRequest);

        call.enqueue(new Callback<AuthResponse>() {
            @Override
            public void onResponse(Call<AuthResponse> call, Response<AuthResponse> response) {
                if (!response.isSuccessful()) {
                    loginResult.setValue(new LoginResult(R.string.login_failed));
                } else {
                    AuthResponse user = response.body();
                    loginResult.setValue(new LoginResult(new LoggedInUserView(user.user.email, user.user.id, user.accessToken)));
                }
            }

            @Override
            public void onFailure(Call<AuthResponse> call, Throwable t) {
                call.cancel();
                loginResult.setValue(new LoginResult(R.string.login_failed));
            }
        });
    }

    public void loginDataChanged(String username, String password) {
        if (!isUserNameValid(username)) {
            loginFormState.setValue(new LoginFormState(R.string.invalid_username, null));
        } else if (!isPasswordValid(password)) {
            loginFormState.setValue(new LoginFormState(null, R.string.invalid_password));
        } else {
            loginFormState.setValue(new LoginFormState(true));
        }
    }

    // A placeholder username validation check
    private boolean isUserNameValid(String username) {
        if (username == null) {
            return false;
        }
        if (username.contains("@")) {
            return Patterns.EMAIL_ADDRESS.matcher(username).matches();
        } else {
            return !username.trim().isEmpty();
        }
    }

    // A placeholder password validation check
    private boolean isPasswordValid(String password) {
        return password != null && password.trim().length() > 5;
    }
}