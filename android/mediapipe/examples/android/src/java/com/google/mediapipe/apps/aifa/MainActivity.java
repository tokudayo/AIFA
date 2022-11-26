package com.google.mediapipe.apps.aifa;

import android.os.Bundle;
import android.view.View;
import android.view.Menu;
import android.util.Log;
import android.content.SharedPreferences;

import com.google.android.material.snackbar.Snackbar;
import com.google.android.material.navigation.NavigationView;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.appcompat.app.AppCompatActivity;

import java.util.HashSet;
import java.util.Set;

public class MainActivity extends AppCompatActivity {

    private AppBarConfiguration mAppBarConfiguration;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setSupportActionBar(findViewById(R.id.toolbar));
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        mAppBarConfiguration = new AppBarConfiguration.Builder(
                  R.id.nav_home, 
                  R.id.nav_login, 
                  R.id.nav_signup,
                  R.id.nav_logout
                )
                .setDrawerLayout(drawer)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        NavigationUI.setupActionBarWithNavController(this, navController, mAppBarConfiguration);
        NavigationUI.setupWithNavController(navigationView, navController);
        this.reloadNavbar();
    }

    public void reloadNavbar() {
        SharedPreferences sp = this.getSharedPreferences("Login", 0);
        Integer userId = sp.getInt("userId", 0);
        String email = sp.getString("email", "");
        NavigationView navigationView = findViewById(R.id.nav_view);
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        Menu menu = navigationView.getMenu();

        if (userId == 0) {
            menu.findItem(R.id.nav_home).setVisible(false);
            menu.findItem(R.id.nav_login).setVisible(true);
            menu.findItem(R.id.nav_signup).setVisible(true);
            menu.findItem(R.id.nav_logout).setVisible(false);

            navController.navigate(R.id.nav_login);
        } else {
            menu.findItem(R.id.nav_home).setVisible(true);
            menu.findItem(R.id.nav_login).setVisible(false);
            menu.findItem(R.id.nav_signup).setVisible(false);
            menu.findItem(R.id.nav_logout).setVisible(true);

            navController.navigate(R.id.nav_home);
        }
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        return NavigationUI.navigateUp(navController, mAppBarConfiguration)
                || super.onSupportNavigateUp();
    }
}