# EMA Filters

[Exponential smoothing or exponential moving average (EMA)](https://en.wikipedia.org/wiki/Exponential_smoothing) is one of many window functions commonly applied to smooth data in signal processing, acting as low-pass filters to remove high-frequency noise.

The library implements a lowpass filter, a highpass filter, and a bandpass filter using EMA, inspired by [this tutorial](https://www.norwegiancreations.com/2016/03/arduino-tutorial-simple-high-pass-band-pass-and-band-stop-filtering/).

The main advantage of this package is that it can calculate the smoothing factor $\alpha$ for EMA from the cutoff frequency and the sampling frequency, based on [this formula](https://en.wikipedia.org/wiki/Low-pass_filter#Simple_infinite_impulse_response_filter).
