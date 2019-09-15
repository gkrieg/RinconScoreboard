import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import pygame
from time import sleep
from ftdi.dmx_controller.OpenDmxUsb import OpenDmxUsb
import time
import os
import random
######################
#     Ideas          #
# Put many different sounds in a list and play one at random
# Make 2 buttons only connect to sounds and then make 2 buttons actually change the scores
#
#####################
def deputy_button_callback(channel):
    global deputies
    global sounds
    global soundsnames
    rand = random.randint(0,len(sounds) - 1)
    sounds[rand].play()
    deputies += 1
    print("deputies: {}".format(deputies))
    outf = open('scores.txt','w')
    outf.write('{}\n{}'.format(outlaws,deputies))
    outf.close()
    t_end = time.time() + .25 
    while time.time() < t_end:
        t.send_dmx([255,0,0,255])
def outlaw_button_callback(channel):
    global outlaws
    global sounds
    global soundsnames
    rand = random.randint(0,len(sounds) - 1)
    sounds[rand].play()
    #global dev
    outlaws += 1
    print("outlaws: {}".format(outlaws))
    outf = open('scores.txt','w')
    outf.write('{}\n{}'.format(outlaws,deputies))
    outf.close()

    t_end = time.time() + .25 
    while time.time() < t_end:
        t.send_dmx([255,255,0,0])
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
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=outlaw_button_callback,bouncetime=800) # Setup event on pin 10 rising edge
GPIO.add_event_detect(5,GPIO.RISING,callback=deputy_button_callback,bouncetime=800) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
