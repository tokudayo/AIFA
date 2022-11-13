package com.google.mediapipe.apps.aifa.ui.signup;

import android.util.Patterns;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.google.mediapipe.apps.aifa.R;
import com.google.mediapipe.apps.aifa.data.APIInterface;
import com.google.mediapipe.apps.aifa.data.SignupRepository;
import com.google.mediapipe.apps.aifa.data.pojo.SignUpRequest;
import com.google.mediapipe.apps.aifa.data.pojo.SignUpResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignupViewModel extends ViewModel {

    private MutableLiveData<SignupFormState> signupFormState = new MutableLiveData<>();
    private MutableLiveData<SignupResult> signupResult = new MutableLiveData<>();
    private SignupRepository signupRepository;

    SignupViewModel(SignupRepository signupRepository) {
        this.signupRepository = signupRepository;
    }

    LiveData<SignupFormState> getSignupFormState() {
        return signupFormState;
    }

    LiveData<SignupResult> getSignupResult() {
        return signupResult;
    }

    public void signup(APIInterface apiInterface, String username, String password, String passwordConfirmation) {
        // can be launched in a separate asynchronous job
        /**
         Create new user
         **/
        SignUpRequest authRequest = new SignUpRequest(username, password, passwordConfirmation);
        Call<SignUpResponse> call = apiInterface.signup(authRequest);

        call.enqueue(new Callback<SignUpResponse>() {
            @Override
            public void onResponse(Call<SignUpResponse> call, Response<SignUpResponse> response) {
                if (!response.isSuccessful()) {
                    signupResult.setValue(new SignupResult(R.string.signup_failed));
                } else {
                    SignUpResponse user = response.body();
                    signupResult.setValue(new SignupResult(new SignedUpUserView(user.email)));
                }
            }

            @Override
            public void onFailure(Call<SignUpResponse> call, Throwable t) {
                call.cancel();
                signupResult.setValue(new SignupResult(R.string.signup_failed));
            }
        });
    }

    public void signupDataChanged(String username, String password) {
        if (!isUserNameValid(username)) {
            signupFormState.setValue(new SignupFormState(R.string.invalid_username, null));
        } else if (!isPasswordValid(password)) {
            signupFormState.setValue(new SignupFormState(null, R.string.invalid_password));
        } else {
            signupFormState.setValue(new SignupFormState(true));
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