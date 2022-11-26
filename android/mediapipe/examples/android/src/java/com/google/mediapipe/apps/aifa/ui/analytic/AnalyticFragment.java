package com.google.mediapipe.apps.aifa.ui.analytic;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.content.SharedPreferences;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.mediapipe.apps.aifa.R;
import com.google.mediapipe.apps.aifa.data.APIClient;
import com.google.mediapipe.apps.aifa.data.APIInterface;
import com.google.mediapipe.apps.aifa.data.pojo.Analytic;

import java.util.ArrayList;
import java.util.Arrays;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class AnalyticFragment extends Fragment {

    private static RecyclerView.Adapter adapter;
    private RecyclerView.LayoutManager layoutManager;
    private static RecyclerView recyclerView;
    private static ArrayList<DataModel> data;
    APIInterface apiInterface;

    public View onCreateView(@NonNull LayoutInflater inflater,
            ViewGroup container, Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_analytic, container, false);

        return root;
    }

    public void onViewCreated(View view,
            Bundle savedInstanceState) {
        recyclerView = view.findViewById(R.id.my_recycler_view);
        recyclerView.setHasFixedSize(true);

        layoutManager = new LinearLayoutManager(getActivity());
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setItemAnimator(new DefaultItemAnimator());

        apiInterface = APIClient.getClient().create(APIInterface.class);
        SharedPreferences sp = this.getContext().getSharedPreferences("Login", 0);
        String accessToken = sp.getString("accessToken", "");

        Log.d("DMM", "Bearer " + accessToken);

        Call<Analytic[]> call = apiInterface.getAnalytics(
                "Bearer " + accessToken);
        data = new ArrayList<>();

        call.enqueue(new Callback<Analytic[]>() {
            @Override
            public void onResponse(Call<Analytic[]> call, Response<Analytic[]> response) {
                if (response.isSuccessful()) {
                    Analytic[] analytics = response.body();

                    for (int i = 0; i < analytics.length; i++) {
                        data.add(new DataModel(
                                analytics[i].exercise,
                                analytics[i].platform,
                                analytics[i].correct,
                                analytics[i].startTime,
                                analytics[i].endTime));
                    }
                    adapter = new CustomAdapter(data);
                    recyclerView.setAdapter(adapter);
                }
            }

            @Override
            public void onFailure(Call<Analytic[]> call, Throwable t) {
                call.cancel();
            }
        });
    }
}