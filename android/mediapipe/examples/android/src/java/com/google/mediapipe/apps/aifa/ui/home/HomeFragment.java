package com.google.mediapipe.apps.aifa.ui.home;

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
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.google.mediapipe.apps.aifa.R;
import com.google.android.material.navigation.NavigationView;

import com.google.mediapipe.apps.aifa.ui.home.StreamFragment;

import org.w3c.dom.Text;

public class HomeFragment extends Fragment {
    private String[] items = new String[]{"Shoulder Press", "Deadlift", "Hammer Curl"};
    private String[] values = new String[]{"shoulder_press", "deadlift", "hammer_curl"};
    private Fragment frag;

    public View onCreateView(@NonNull LayoutInflater inflater,
            ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);
        View root = inflater.inflate(R.layout.fragment_home, container, false);

        Spinner dropdown = root.findViewById(R.id.spinner);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(getActivity(), android.R.layout.simple_spinner_dropdown_item, items);
        dropdown.setAdapter(adapter);

        return root;
    }

    public void onViewCreated(View view,
            Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        super.onActivityCreated(savedInstanceState);

        final Spinner spinner = view.findViewById(R.id.spinner);
        final Button startButton = view.findViewById(R.id.start);
        final Button stopButton = view.findViewById(R.id.stop);

        startButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                frag = StreamFragment.newInstance(values[spinner.getSelectedItemPosition()]);
                FragmentTransaction ft = getFragmentManager().beginTransaction();
                spinner.setVisibility(View.INVISIBLE);
                startButton.setVisibility(View.INVISIBLE);
                stopButton.setVisibility(View.VISIBLE);
                ft.replace(R.id.container, frag);
                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE);
                ft.addToBackStack(null);
                ft.commit();
                // loginViewModel.login(apiInterface, usernameEditText.getText().toString());
            }
        });

        stopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FragmentTransaction ft = getFragmentManager().beginTransaction();
                spinner.setVisibility(View.VISIBLE);
                startButton.setVisibility(View.VISIBLE);
                stopButton.setVisibility(View.INVISIBLE);
                ft.remove(frag).commit();
            }
        });
    }
}