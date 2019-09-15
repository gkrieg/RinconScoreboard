# RinconScoreboard

To install, start a new virtual environment and run
```
pip install -r requirements.txt
```

You will also need to place the file 98-uDMX.rules in your /etc/udev/rules.d/ folder and then you must restart your raspberry pi. This is a udev rule, which gives permissions to interface with the ftdi usb to DMX cable for the DMX lighting.

The wiring for the raspberry pi is shown in the scoreboard.py near the beginning of the file. It just follows absolute pin location (so you don't have to know the names of the different pins).
