package com.google.mediapipe.apps.aifa.ui.logout;

import android.app.Activity;
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
import android.content.SharedPreferences;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.google.mediapipe.apps.aifa.R;
import com.google.mediapipe.apps.aifa.MainActivity;
import com.google.android.material.navigation.NavigationView;

import org.w3c.dom.Text;

public class LogoutFragment extends Fragment {

    public View onCreateView(@NonNull LayoutInflater inflater,
            ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);
        View root = inflater.inflate(R.layout.fragment_logout, container, false);

        return root;
    }

    public void onViewCreated(View view,
            Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        super.onActivityCreated(savedInstanceState);

        NavigationView navigationView = getActivity().findViewById(R.id.nav_view);
        View headerView = navigationView.getHeaderView(0);
        TextView textView = headerView.findViewById(R.id.textView);
        textView.setText("");

        SharedPreferences sp = this.getContext().getSharedPreferences("Login", 0);
        SharedPreferences.Editor Ed = sp.edit();
        Ed.putInt("userId", 0);
        Ed.putString("email", "");
        Ed.commit();
        ((MainActivity) getActivity()).reloadNavbar();
    }
}