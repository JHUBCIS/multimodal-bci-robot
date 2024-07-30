#ifndef EMA_Filters_h
#define EMA_Filters_h

#include "Arduino.h"

class EMA_Filters {
  public:
    EMA_Filters();
    float LPF(float input, float f_c, float f_s);  // lowpass filter
    float HPF(float input, float f_c, float f_s);  // highpass filter
    float BPF(float input, float f_c_low, float f_c_high, float f_s);  // bandpass filter
    
  private:
    float prev_ema_lp, prev_ema_hp, prev_ema_bplow, prev_ema_bphigh;
    float alpha(float f_s, float f_c);
};

#endif