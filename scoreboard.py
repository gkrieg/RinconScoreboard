import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import pygame
from time import sleep
from ftdi.dmx_controller.OpenDmxUsb import OpenDmxUsb
import time
import os
import random
import board
import adafruit_dotstar as dotstar
######################
#     Ideas          #
# Put many different sounds in a list and play one at random
# Make 2 buttons only connect to sounds and then make 2 buttons actually change the scores
#
#####################



def deputy_button_callback(channel):
    global sounds
    global soundsnames
    rand = random.randint(0,len(sounds) - 1)
    sounds[rand].play()
    t_end = time.time() + .25 
    while time.time() < t_end:
        t.send_dmx([255,0,0,255])



def outlaw_button_callback(channel):
    rand = random.randint(0,len(sounds) - 1)
    sounds[rand].play()
    t_end = time.time() + .25 
    while time.time() < t_end:
        t.send_dmx([255,255,0,0])

def real_deputy_button_callback(channel):
    global outlaws
    global deputies
    deputies += 1
    print("deputies: {}".format(deputies))
    outf = open('scores.txt','w')
    outf.write('{}\n{}'.format(outlaws,deputies))
    outf.close()
    update_LEDs()

def real_outlaw_button_callback(channel):
    global outlaws
    global deputies
    outlaws += 1
    print("outlaws: {}".format(outlaws))
    outf = open('scores.txt','w')
    outf.write('{}\n{}'.format(outlaws,deputies))
    outf.close()
    update_LEDs()

def update_LEDs():
    global outlaws
    global deputies
    global dots
    if outlaws > 0 and deputies > 0:
        centerpos = int(outlaws / (outlaws + deputies) * 144)
        centerval = (int((1 - (outlaws / (outlaws + deputies))) * 255),0,int(outlaws / (outlaws + deputies) * 255))
    else:
        centerpos = 144 / 2
        centerval = (128,0,128)

    for i in range(144):
        if i < centerpos - 5:
            dots[i] = (255,0,0)
        elif i < centerpos + 5:
            dots[i] = centerval
        else:
            dots[i] = (0,0,255)


def load_sounds():
    sounds = []
    soundsnames = []
    for f in os.listdir('sounds'):
        sounds.append(pygame.mixer.Sound('sounds/' + f))
        soundsnames.append(f)
    return sounds,soundsnames

inf = open('scores.txt','r').readlines()
outlaws = int(inf[0].strip())
deputies = int(inf[1].strip())
pygame.init()
t = OpenDmxUsb()
sounds,soundsnames = load_sounds()



GPIO.setwarnings(False) # Ignore warning for now
print(GPIO.getmode())
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
dots = dotstar.DotStar(board.SCK, board.MOSI, 144, brightness=0.2)
for i in range(144):
    if i < 70:
        dots[i] = (255,0,0)
    elif i < 74:
        dots[i] = (128,0,128)
    else:
        dots[i] = (0,0,255)
GPIO.add_event_detect(15,GPIO.RISING,callback=outlaw_button_callback,bouncetime=800) # Setup event on pin 10 rising edge
GPIO.add_event_detect(3,GPIO.RISING,callback=deputy_button_callback,bouncetime=800) # Setup event on pin 10 rising edge
GPIO.add_event_detect(19,GPIO.RISING,callback=real_outlaw_button_callback,bouncetime=800) # Setup event on pin 10 rising edge
GPIO.add_event_detect(26,GPIO.RISING,callback=real_deputy_button_callback,bouncetime=800) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
