# RinconScoreboard

To install, start a new virtual environment and run
```
pip install -r requirements.txt
```
This requires Python 3.6 or later (to work with pygame and ftdi).

You will also need to place the file 98-uDMX.rules in your /etc/udev/rules.d/ folder and then you must restart your raspberry pi. This is a udev rule, which gives permissions to interface with the ftdi usb to DMX cable for the DMX lighting.

The wiring for the raspberry pi is shown in the scoreboard.py near the beginning of the file. 
