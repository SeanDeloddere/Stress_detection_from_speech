package be.upcast.experiment;

import android.os.Bundle;
import android.view.View;
import android.widget.SeekBar;
import android.widget.TextView;

import be.upcast.experiment.models.ParticipantModel;

public class SlidersActivity extends FullscreenActivity {
    public static ParticipantModel p;
    private SeekBar MOE;
    private SeekBar KRACHTIG;
    private SeekBar BOOS;
    private SeekBar TEVREDEN;
    private SeekBar GESPANNEN;
    private SeekBar NEERSLACHTIG;
    private SeekBar PRETTIG;

    private TextView Moe;
    private TextView Krachtig;
    private TextView Boos;
    private TextView Tevreden;
    private TextView Gespannen;
    private TextView Neerslachtig;
    private TextView Prettig;

    private int MoeScore;
    private int KrachtigScore;
    private int BoosScore;
    private int TevredenScore;
    private int GespannenScore;
    private int NeerslachtigScore;
    private int PrettigScore;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sliders);

        Moe = (TextView) findViewById(R.id.Moe);
        MOE = (SeekBar)findViewById(R.id.seekBar10);
        MOE.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                MoeScore = progress;
                Moe.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        Krachtig = (TextView) findViewById(R.id.Krachtig);
        KRACHTIG = (SeekBar)findViewById(R.id.seekBar11);
        KRACHTIG.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                KrachtigScore = progress;
                Krachtig.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        Boos = (TextView) findViewById(R.id.Boos);
        BOOS = (SeekBar)findViewById(R.id.seekBar12);
        BOOS.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                BoosScore = progress;
                Boos.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        Tevreden = (TextView) findViewById(R.id.Tevreden);
        TEVREDEN = (SeekBar)findViewById(R.id.seekBar13);
        TEVREDEN.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                TevredenScore = progress;
                Tevreden.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        Gespannen = (TextView) findViewById(R.id.Gespannen);
        GESPANNEN = (SeekBar)findViewById(R.id.seekBar14);
        GESPANNEN.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                GespannenScore = progress;
                Gespannen.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        Neerslachtig = (TextView) findViewById(R.id.Neerslachtig);
        NEERSLACHTIG = (SeekBar)findViewById(R.id.seekBar15);
        NEERSLACHTIG.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                NeerslachtigScore = progress;
                Neerslachtig.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        Prettig = (TextView) findViewById(R.id.Prettig);
        PRETTIG = (SeekBar)findViewById(R.id.seekBar16);
        PRETTIG.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                PrettigScore = progress;
                Prettig.setText(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });


    }

    public void next(View v) {
        if(p.VAS==1){
            p.Vas1.put("Moe",MoeScore);
            p.Vas1.put("Krachtig",KrachtigScore);
            p.Vas1.put("Boos",BoosScore);
            p.Vas1.put("Tevreden",TevredenScore);
            p.Vas1.put("Gespannen",GespannenScore);
            p.Vas1.put("Neerslachtig",NeerslachtigScore);
            p.Vas1.put("Prettig",PrettigScore);
        } else if(p.VAS==2){
            p.Vas2.put("Moe",MoeScore);
            p.Vas2.put("Krachtig",KrachtigScore);
            p.Vas2.put("Boos",BoosScore);
            p.Vas2.put("Tevreden",TevredenScore);
            p.Vas2.put("Gespannen",GespannenScore);
            p.Vas2.put("Neerslachtig",NeerslachtigScore);
            p.Vas2.put("Prettig",PrettigScore);
        } else{
            p.Vas3.put("Moe",MoeScore);
            p.Vas3.put("Krachtig",KrachtigScore);
            p.Vas3.put("Boos",BoosScore);
            p.Vas3.put("Tevreden",TevredenScore);
            p.Vas3.put("Gespannen",GespannenScore);
            p.Vas3.put("Neerslachtig",NeerslachtigScore);
            p.Vas3.put("Prettig",PrettigScore);
        }
    }
}
