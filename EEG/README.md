# EEG-ExPy_JHUBCIS

See the original [EEG-ExPy](https://github.com/NeuroTechX/EEG-ExPy) Github page, the [NTX documentation](https://neurotechx.github.io/EEG-ExPy/) page, as well as the the [doc](./doc) directory in this repo for main documentations. This readme is compiled by JHUBCIS as an addition to the original documentation.

## Installation

Unless you would like to update the repository, it is recommended to download the repo as a zip file, unpack to a local directory, and run the repo in a `conda` virtual environment with [miniconda](https://docs.anaconda.com/free/miniconda/). Python 3.9.19 should work. To create a named `conda` virtual environment in command line and set it up with all the dependencies, try:

```powershell
cd "[your local directory]\EEG-ExPy_JHUBCIS"

conda create -n "eeg-expy-py3.9" python=3.9 

conda activate "eeg-expy-py3.9"

pip install -r requirements.txt
```

Note that you should replace `[your local directory]` with the directory of where you have actually unpacked the zip file.

The [Unicorn Suite](https://www.gtec.at/product/unicorn-suite/) software is recomended to run this repo with the [Unicorn Hybrid Black](https://www.gtec.at/product/unicorn-hybrid-black/) headset, which only runs on Windows. 🥲

Please refer to the [unicorn-bi](https://github.com/unicorn-bi) Github page by g.tec for more resources and documentation.

Note that the original EEG-ExPy repo is also compatible with many other EEG headsets that are compatible with other operating systems. The EEG-ExPy_JHUBCIS repo may be further updated so that the custom code added by JHUBCIS may be compatible with other EEG headsets supported by the original EEG-ExPy repo.

## Connecting to Unicorn Hybrid Black

To ensure the Unicorn Hybrid Black headset is connected and has good signal quality, it is suggested to use the Unicorn Suite software to vefiry.

To connect for the first time, make sure to activate Unicron Suite using the lisence information provided with your Unicorn Hybrid Black headset. Go to *Unicorn Suite Hybrid Black > Lisences > Add Lisence* and enter the information.

On how to use the Unicorn Suite software to establish connection, you may refer to the [Unicorn Suite Hybrid Black User Manual](https://github.com/unicorn-bi/Unicorn-Suite-Hybrid-Black-User-Manual) on Github or [UnicornSuite.pdf](doc/UnicornSuite.pdf) in this repo. Note that the pdf is only the documentation for Unicorn Suite 1.18.00.

However, we have noticed that not every step in the manual is necessary. Often the following steps would be sufficient:

1. insert the bluetooth dongle to your Windows pc
2. Go to *Unicorn Suite Hybrid Black > My Unicorn* and click on the serial number of the headset you want to conect to in the middle panel
3. The headset should be properly connected when it shows up on the third panel in that page

Once the headset is connected, help the user put it on ([here is a video guide](https://www.youtube.com/watch?v=UVVUJTwvGnw)), and go to Unicorn Recorder or Unicorn Bandpower to test the signal quality.

- After either app is booted, on the right end of the window there will be an icon of the brain with circular cues to indicate the signal quality from each electrode. Green for good, yellow for moderate, and red for bad.

after all setup is complete and signal quality is checked to be good, make sure to close the Unicorn Suite software so that you may access the headset from the code in the repo.

## Streaming from Unicorn Hybrid Black

Run the [run_stream.py](./run_stream.py) in the python virtual environment created for the repo.

The `stream_plot()` function is defined in [eegnb/devices/eeg.py](eegnb/devices/eeg.py), with custom components from [eeg_rt_plot_mpl.py](eegnb/devices/eeg_rt_plot_mpl.py), [rolling_buffer.py](eegnb/devices/rolling_buffer.py), and [EMA_Filters.py](eegnb/devices/EMA_Filters.py). The function allows streaming filtered (bandpass and notch) EEG electrode data from the Unicorn Hybrid Black headset, and saving the streamed data.

First press 'q' to stop stream and save data, then close plot window to end program.

## Running the VisualSSVEP_select Experiment on Unicorn Hybrid Black

### Without Unicorn Recorder

Run the [run_experiment.py](./run_expriment.py). This is a template that can also be used to run other experiemnts, but is currently set to run the [VisualSSVEP_select](eegnb/experiments/visual_ssvep/ssvep_select.py) Experiment. You may specify `subject_id`, `session_nb`, and `record_duration` as you like.

The experiment collects filtered (bandpass and notch) EEG data while the subject may choose to focus their visual attention on one of the two visual stimuli is the left and right corners of the screen. You may specify the flashing frequency of the left and right stimuli with the `freq1` and `freq2` parameters respectively. See [Multi-frequency steady-state visual evoked potential dataset](https://www.nature.com/articles/s41597-023-02841-5) on how to choose these values.

After the experiment is done, please use the [ssvep_select-clean_data.ipynb](eegnb/experiments/visual_ssvep/ssvep_select-clean_data.ipynb) to clean up the formatting.

### With Unicorn Recorder

Since Release 1.24, [Unicorn Recorder](https://github.com/unicorn-bi/Unicorn-Recorder-Hybrid-Black) has included the [OSCAR](https://github.com/unicorn-bi/Unicorn-Recorder-Hybrid-Black?tab=readme-ov-file#oscar) artifact removal algorithm, as well as a feature to [log triggers through UDP](https://github.com/unicorn-bi/Unicorn-Recorder-Hybrid-Black?tab=readme-ov-file#receiving-triggers-via-udp).

First make sure Unicorn Recorder is running and can stream data from the Unicorn headset. Then stop and start a new recording session. It is strongly suggested that all options be selected in [Acquisition settings](https://github.com/unicorn-bi/Unicorn-Recorder-Hybrid-Black?tab=readme-ov-file#acquisition-settings) so that it is easier to clean up the output csv.

Configure the IP address and port in the Run [run_experiment_unicorn.py](run_expriment_unicorn.py). Enter the corresponding IP address and UDP port number as parameters of the experiment. e.g.

```python
experiment = VisualSSVEP_select_unicorn(duration=record_duration, freq1=7, freq2=23, IP="127.0.0.1", Port=1000)
```

> In case there seems to be issues with UDP:
>
> 1. First make sure to add a rule in `Windows Defender Firewall with Advanced Security` to allow UDP traffic on the port of your choice. This can be done via GUI, or through command line run as administrator. e.g.
>
>    ```powershell
>       netsh advfirewall firewall add rule name="Open UDP Port 1000" dir=in action=allow protocol=UDP localport=1000
>    ```
> 2. While the Unicorn Recorder is closed, try [UDP_listener_test.ps1](UDP_listener_test.ps1). This is a powershell script that sets up a UDP listener ofa UDP port (1000 by default). Run this script in powershell, then run the experiment. Try logging markers using left and right arrow keys, and if the UDP port is working, you should see output similar to the following:
>
>    ```powershell
>       PS ~\Documents\GitHub\EEG-ExPy_JHUBCIS> .\UDP_listener_test.ps1
>       Listening for UDP packets on port 1000...
>       Received data: 1 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>       Received data: 2 from 127.0.0.1:57848
>    ```
>
>    Once verified, the Unicorn Recorder should be able to pick up key presses.
>    When proceeding to run actual experiment, make sure to stop `UDP_listener_test.ps1` by killing the terminal or other means so that the Unicorn Recorder can receive key presses.

When the experiment is done, stop recording on Unicorn Recorder and [export the data as csv](https://github.com/unicorn-bi/Unicorn-Recorder-Hybrid-Black?tab=readme-ov-file#recording-settings). Then use the [ssvep_select_unicorn-clean_data.ipynb](eegnb/experiments/visual_ssvep/ssvep_select_unicorn-clean_data.ipynb) to clean up the formatting.
