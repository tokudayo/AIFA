package com.google.mediapipe.apps.aifa.ui.signup;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.google.mediapipe.apps.aifa.R;
import com.google.mediapipe.apps.aifa.data.APIClient;
import com.google.mediapipe.apps.aifa.data.APIInterface;

public class SignupFragment extends Fragment {

    private SignupViewModel signupViewModel;
    APIInterface apiInterface;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);
        View root = inflater.inflate(R.layout.fragment_signup, container, false);

        return root;
    }

    public void onViewCreated(View view,
                              Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        super.onActivityCreated(savedInstanceState);
        signupViewModel = new ViewModelProvider(this, new SignupViewModelFactory())
                .get(SignupViewModel.class);

        final EditText usernameEditText = view.findViewById(R.id.username);
        final EditText passwordEditText = view.findViewById(R.id.password);
        final EditText passwordConfirmationEditText = view.findViewById(R.id.password_confirmation);
        final Button signupButton = view.findViewById(R.id.signup);
        final ProgressBar loadingProgressBar = view.findViewById(R.id.loading);
        apiInterface = APIClient.getClient().create(APIInterface.class);

        signupViewModel.getSignupFormState().observe(getViewLifecycleOwner(), new Observer<SignupFormState>() {
            @Override
            public void onChanged(@Nullable SignupFormState signupFormState) {
                if (signupFormState == null) {
                    return;
                }
                signupButton.setEnabled(signupFormState.isDataValid());
                if (signupFormState.getUsernameError() != null) {
                    usernameEditText.setError(getString(signupFormState.getUsernameError()));
                }
                if (signupFormState.getPasswordError() != null) {
                    passwordEditText.setError(getString(signupFormState.getPasswordError()));
                }
            }
        });

        signupViewModel.getSignupResult().observe(getViewLifecycleOwner(), new Observer<SignupResult>() {
            @Override
            public void onChanged(@Nullable SignupResult signupResult) {
                if (signupResult == null) {
                    return;
                }
                loadingProgressBar.setVisibility(View.GONE);
                if (signupResult.getError() != null) {
                    showSignupFailed(signupResult.getError());
                }
                if (signupResult.getSuccess() != null) {
                    updateUiWithUser(signupResult.getSuccess());
                    Navigation.findNavController(view).navigate(R.id.nav_login);
                }
            }
        });

        TextWatcher afterTextChangedListener = new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                // ignore
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                // ignore
            }

            @Override
            public void afterTextChanged(Editable s) {
                signupViewModel.signupDataChanged(usernameEditText.getText().toString(),
                        passwordEditText.getText().toString());
            }
        };
        usernameEditText.addTextChangedListener(afterTextChangedListener);
        passwordEditText.addTextChangedListener(afterTextChangedListener);
        passwordConfirmationEditText.addTextChangedListener(afterTextChangedListener);

        signupButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loadingProgressBar.setVisibility(View.VISIBLE);
                signupViewModel.signup(apiInterface, usernameEditText.getText().toString(),
                        passwordEditText.getText().toString(), passwordConfirmationEditText.getText().toString());
            }
        });
    }

    private void updateUiWithUser(SignedUpUserView model) {
        String signup_success = getString(R.string.signup_success) + model.getDisplayName();
        Toast.makeText(getActivity(), signup_success, Toast.LENGTH_LONG).show();
    }

    private void showSignupFailed(@StringRes Integer errorString) {
        Toast.makeText(getActivity(), errorString, Toast.LENGTH_SHORT).show();
    }
}