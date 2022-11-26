package com.google.mediapipe.apps.aifa.ui.analytic;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.google.mediapipe.apps.aifa.R;

import java.util.ArrayList;

public class CustomAdapter extends RecyclerView.Adapter<CustomAdapter.MyViewHolder> {
    private ArrayList<DataModel> dataSet;

    public static class MyViewHolder extends RecyclerView.ViewHolder {

        TextView textViewExercise;
        TextView textViewPlatform;
        TextView textViewCorrect;
        TextView textViewStartTime;
        TextView textViewEndTime;

        public MyViewHolder(View itemView) {
            super(itemView);
            this.textViewExercise = itemView.findViewById(R.id.exercise);
            this.textViewPlatform = itemView.findViewById(R.id.platform);
            this.textViewCorrect = itemView.findViewById(R.id.correct);
            this.textViewStartTime = itemView.findViewById(R.id.start_time);
            this.textViewEndTime = itemView.findViewById(R.id.end_time);
        }
    }

    public CustomAdapter(ArrayList<DataModel> data) {
        this.dataSet = data;
    }

    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent,
                                           int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.cards_layout, parent, false);

        MyViewHolder myViewHolder = new MyViewHolder(view);
        return myViewHolder;
    }

    @Override
    public void onBindViewHolder(final MyViewHolder holder, final int listPosition) {

        TextView textViewExercise = holder.textViewExercise;
        TextView textViewPlatform = holder.textViewPlatform;
        TextView textViewCorrect = holder.textViewCorrect;
        TextView textViewStartTime = holder.textViewStartTime;
        TextView textViewEndTime = holder.textViewEndTime;

        textViewExercise.setText(dataSet.get(listPosition).getExercise());
        textViewPlatform.setText(dataSet.get(listPosition).getPlatform());
        textViewCorrect.setText(dataSet.get(listPosition).getCorrect());
        textViewStartTime.setText(dataSet.get(listPosition).getStartTime());
        textViewEndTime.setText(dataSet.get(listPosition).getEndTime());
    }

    @Override
    public int getItemCount() {
        return dataSet.size();
    }
}
