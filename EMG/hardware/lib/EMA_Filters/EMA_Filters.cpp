#include "EMA_Filters.h"

EMA_Filters::EMA_Filters() {
  prev_ema_lp = 0;
  prev_ema_hp = 0;
  prev_ema_bplow = 0;
  prev_ema_bphigh = 0;
}

/* Calculate weighing factor for EMA from cutoff frequency
float f_c: cutoff frequency
float f_s: sampling frequency
*/ 
float EMA_Filters::alpha(float f_s, float f_c) {
  return (2 * PI * (1 / f_s) * f_c)/(2 * PI * (1 / f_s) * f_c + 1);
}

/* EMA for lowpass filter as it is
float input: input signal
float f_c: cutoff frequency
float f_s: sampling frequency
*/
float EMA_Filters::LPF(float input, float f_c, float f_s) {
  float alphaValue = alpha(f_s, f_c);
  float ema_lp = (1 - alphaValue) * prev_ema_lp + alphaValue * input;
  prev_ema_lp = ema_lp;  // Update the previous EMA value for the next call
  return ema_lp;
}

/* highpass filter: subtracting the lowpass from the original
float input: input signal
float f_c: cutoff frequency
float f_s: sampling frequency
*/
float EMA_Filters::HPF(float input, float f_c, float f_s) {
  float alphaValue = alpha(f_s, f_c);
  float ema_hp = (1 - alphaValue) * prev_ema_hp + alphaValue * input;
  prev_ema_hp = ema_hp;  // Update the previous EMA value for the next call
  float hp = input - ema_hp;  // Subtract the lowpass output from the raw input
  return hp;
}

/* bandpass filter: subtracting 2 lowpass results
float input: input signal
float f_c_low: lower cutoff frequency
float f_c_high: higher cutoff frequency
float f_s: sampling frequency
*/
float EMA_Filters::BPF(float input, float f_c_low, float f_c_high, float f_s) {
  float alphaValueLow = alpha(f_s, f_c_low);
  float alphaValueHigh = alpha(f_s, f_c_high);
  
  float ema_bplow = (1 - alphaValueLow) * prev_ema_bplow + alphaValueLow * input;
  prev_ema_bplow = ema_bplow;  // Update the previous EMA value for the next call
  
  float highpassOutput = input - ema_bplow;  // High-pass filter
  
  float ema_bphigh = (1 - alphaValueHigh) * prev_ema_bphigh + alphaValueHigh * highpassOutput;
  prev_ema_bphigh = ema_bphigh;  // Update the previous EMA value for the next call
  
  return ema_bphigh;  // bandpass filter output
}