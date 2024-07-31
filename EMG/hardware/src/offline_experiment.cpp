#include <Arduino.h>
#include <EMA_Filters.h>
#include <RunningAverage.h>
#include <NoDelay.h>
#include <Servo.h>

/*create instances for data processing*/
EMA_Filters emaFilt0; 
EMA_Filters emaFilt1; 
// EMA_Filters emaFilt2; 
float f_s = 400; // sampling frequency
const int avg_window = 10;
RunningAverage rnAvg0(avg_window);
RunningAverage rnAvg1(avg_window);

/*EMG parameters*/
int emg_pin0 = 0; // analog input pin
int emg_pin1 = 1; // analog input pin

float emg_stat0 = 0; // resting EMG signal
float emg_stat1 = 0; // resting EMG signal

/*button parameters*/
const int buttonPin0 = 4;  // the number of the pushbutton pin
const int buttonPin1 = 7;  // the number of the pushbutton pin

int buttonState0 = 0;  // variable for reading the pushbutton status
int buttonState1 = 0;  // variable for reading the pushbutton status

const int ledPin = 12;    // the number of the LED pin

void setup() {
  Serial.begin(115200);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);

  // initialize the pushbutton pin as an input:
  pinMode(buttonPin0, INPUT);
  pinMode(buttonPin1, INPUT);

  /*resting EMG signal collection for calibration*/ 
  // Serial.println("Resting EMG collection for calibration");
  float emg_stat_sum_0 = 0;
  float emg_stat_sum_1 = 0;

  for (int i=0; i<10; i++)
  {
    Serial.print("Done in ");
    Serial.println(10-i);
    for (int j=0; j<100; j++)
    {
        emg_stat_sum_0 += analogRead(emg_pin0);
        emg_stat_sum_1 += analogRead(emg_pin1);

        delay(10);
    } 
  }
  emg_stat0 = emg_stat_sum_0 / 1000.0;
  emg_stat1 = emg_stat_sum_1 / 1000.0;

  Serial.print("Done! Resting EMG is: ");
  Serial.print(emg_stat0);
  Serial.print("\t");
  Serial.print(emg_stat1);
}



void loop() {
  static unsigned long loopStartTime = millis(); // Track when loop() started, records only once
  unsigned long elapsedTime = millis() - loopStartTime; // Calculate elapsed time
  Serial.print(">elapsed Time (ms): ");
  Serial.println(elapsedTime);

  buttonState0 = digitalRead(buttonPin0);
  buttonState1 = digitalRead(buttonPin1);

  check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
  }

  /*EMG collection and visualization*/
  float emg_raw0 = (analogRead(emg_pin0) - emg_stat0); // raw centered emg signal 
  float emg_raw1 = (analogRead(emg_pin1) - emg_stat1); // raw centered emg signal 

  // bandpass
  float f_c_bplow = 50; // low cut off frequency
  float f_c_bphigh = 150; // high cut off frequency
  float emg_bp0 = emaFilt0.BPF(emg_raw0, f_c_bplow, f_c_bphigh, f_s); // bandpassed emg signal between 50 Hz and 150 Hz
  float emg_bp1 = emaFilt1.BPF(emg_raw1, f_c_bplow, f_c_bphigh, f_s); // bandpassed emg signal between 50 Hz and 150 Hz


  /*capture EMG singal envelope*/
  float f_c_lp = 1; // lowpass cut off frequency 
  float emg_evlp0 =  pow(emaFilt0.LPF(abs(emg_bp0), f_c_lp, f_s), 2); // take magnitude, lowpass, then square
  float emg_evlp1 =  pow(emaFilt1.LPF(abs(emg_bp1), f_c_lp, f_s), 2); // take magnitude, lowpass, then square

  rnAvg0.addValue(emg_evlp0); // update the buffers
  rnAvg1.addValue(emg_evlp1); // update the buffers

  float emg_evlp_avg0 = rnAvg0.getAverage();
  float emg_evlp_avg1 = rnAvg1.getAverage();


  // plot all signals using Teleplot
  Serial.print(">button 0: "); Serial.println(buttonState0);
  Serial.print(">button 1: "); Serial.println(buttonState1);
  
  Serial.print(">raw EMG 0: "); Serial.println(emg_raw0);
  Serial.print(">raw EMG 1: "); Serial.println(emg_raw1);

  // Plot bandpassed EMG signals with Teleplot
  Serial.print(">bandpass EMG 0: ");  Serial.println(emg_bp0);
  Serial.print(">bandpass EMG 1: "); Serial.println(emg_bp1);
  
  Serial.print(">bandpass EMG envelope 0: "); 
  Serial.println((std::string) emg_evlp_avg0 + " " + (std::string) emg_evlp_avg1);
  Serial.print(">bandpass EMG envelope 1: "); Serial.println(emg_evlp_avg1);
}