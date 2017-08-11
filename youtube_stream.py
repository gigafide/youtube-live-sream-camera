#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------
#IMPORT REQUIRED DEPENDENCIES
#----------------------------

import os
import time
import io
import pygame
import picamera
import subprocess

#----------------------------
#SET TFT TOUCHSCREEN TO BE DEFAULT ENVINROMENT
#----------------------------

os.environ['SDL_VIDEODRIVER'] = 'fbcon'					#load the screen driver
os.environ['SDL_FBDEV'] = '/dev/fb1'					#set fb1 screen as default
os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'	#use touchscreen as default
os.environ['SDL_MOUSEDRV'] = 'TSLIB'					#load the mouse driver

#----------------------------
#INITIALIZE PYGAME AND VARIABLES
#----------------------------
pygame.init()											#initialize pygame
lcd = pygame.display.set_mode((0,0), pygame.FULLSCREEN)	#set display mode
pygame.mouse.set_visible(False)							#disable mouse visibility

img_bg = pygame.image.load('camera_bg.jpg')

preview_toggle = 0										#toggle variable for preview mode
stream_toggle = 0										#toggle variable for stream mode

blue = 26, 0, 255										#variable for blue hex color
white = 255, 255, 255									#variable for white hex color
cream = 254, 255, 250									#variable for cream hex color

#----------------------------
#INITIALIZE STREAMING VARIABLES
#----------------------------

YOUTUBE="rtmp://a.rtmp.youtube.com/live2/"				#Youtube stream URL
KEY= #ENTER PRIVATE KEY HERE#							#Youtube stream key

# FFMPEG command for streaming to Youtube
stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -f alsa -ac 1 -i hw:1,0 -vcodec copy -acodec aac -ac 1 -ar 8000 -ab 32k -map 0:0 -map 1:0 -strict experimental -f flv ' + YOUTUBE + KEY 
# Popen command to PIPE from FFMPEG
stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)

#----------------------------
#INITIALIZE CAMERA AND VARIABLES
#----------------------------

camera = picamera.PiCamera()							#initialize camera
camera.resolution = (1080, 720)#(640, 480)				#set camera resolution
camera.rotation   = 180									#set camera rotation
camera.crop       = (0.0, 0.0, 1.0, 1.0)				#camera crop settings
camera.framerate  = 25									#camera framerate settings

#create byte array for storing camera images in buffer
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

#----------------------------
#CREATE A FUNCTION FOR MAKING BUTTONS
#----------------------------

def make_button(text, xpo, ypo, color):
        font=pygame.font.Font(None,24)					#set font
        label=font.render(str(text),1,(color))			#render text
        lcd.blit(label,(xpo,ypo))						#display on LCD
		#draw rectangle around text
        pygame.draw.rect(lcd, cream, (xpo-5,ypo-5,150,35),1)

#----------------------------
#CREATE A FUNCTION ENABLING LIVE STREAM MODE
#----------------------------

def stream():
	camera.wait_recording(1)							#start stream
	
#----------------------------
#CREATE A FUNCTION TO SHUTDOWN THE PI
#----------------------------
def shutdown_pi():
        os.system("sudo shutdown -h now")

#----------------------------
#CREATE A FUNCTION ENABLING PREVIEW STREAM MODE
#----------------------------

def preview():
	stream = io.BytesIO()
	camera.vflip = True
	camera.hflip = True
	camera.capture(stream, use_video_port=True, format='rgb', resize=(320, 240))
	stream.seek(0)
	stream.readinto(rgb)
	stream.close()
	img = pygame.image.frombuffer(rgb[0:(320 * 240 * 3)], (320, 240), 'RGB')
	lcd.blit(img, (0,0))
	make_button("STOP", 175,200, white)
	pygame.display.update()

#----------------------------
#MAIN LOOP
#----------------------------

#try for errors first
try:
	while True:
		#if stream toggle is enabled, run stream mode function
		if stream_toggle == 1:
			stream()
		#if preview toggle is enabled, run preview mode function
		elif preview_toggle == 1:
			preview()
		else:
			click_count = 0		
			lcd.fill(blue)
			lcd.blit(img_bg,(0,0))
			make_button("STREAM", 5, 200, white)
			make_button("PREVIEW",175,200, white)
			make_button("POWER", 200, 5, white)
			pygame.display.update()
		for event in pygame.event.get():
			if (event.type == pygame.MOUSEBUTTONDOWN):
				pos = pygame.mouse.get_pos()
			if (event.type == pygame.MOUSEBUTTONUP):
				pos = pygame.mouse.get_pos()
				print pos
				x,y = pos
				if x < 200 & y > 100:
                                       print "stream pressed"
                                       if stream_toggle == 0 and preview_toggle == 0:
                                               stream_toggle = 1
                                               lcd.fill(blue)
                                               lcd.blit(img_bg,(0,0))
                                               make_button("STOP", 20, 200, white)
                                               pygame.display.update()
                                               camera.vflip=True
                                               camera.hflip = True
                                               camera.start_recording(stream_pipe.stdin, format='h264', bitrate = 2000000)
                                       elif preview_toggle == 1:
                                               preview_toggle = 0
                                               lcd.fill(blue)
                                               lcd.blit(img_bg,(0,0))
                                               make_button("STREAM", 5, 200, white)
                                               make_button("PREVIEW",175,200, white)
                                               pygame.display.update()
                                       else:
                                               stream_toggle = 0
                                               lcd.fill(blue)
                                               make_button("STREAM", 5, 200, white)
                                               make_button("PREVIEW",175,200, white)
                                               pygame.display.update()
                                               camera.stop_recording()
                                elif x > 225 & y > 150:
                                        print "preview pressed"
                                        if preview_toggle == 0 and stream_toggle == 0:
                                                preview_toggle = 1
                                                lcd.fill(blue)
                                                make_button("STOP", 175,200, white)
                                                pygame.display.update()
                                        elif stream_toggle == 1:
                                                stream_toggle = 0
                                                lcd.fill(blue)
                                                make_button("STREAM", 5, 200, white)
                                                make_button("PREVIEW",175,200, white)
                                                pygame.display.update()
                                                camera.stop_recording()
                                        else:
                                                preview_toggle = 0
                                                lcd.fill(blue)
                                                make_button("STREAM", 5, 200, white)
                                                make_button("PREVIEW",175,200, white)
                                                pygame.display.update()
                                elif x > 200 & y < 100:
                                        print "power pressed"
                                        if preview_toggle == 0 and stream_toggle == 0:
                                                shutdown_pi()

except KeyboardInterrupt:
	camera.stop_recording()
	print ' Exit Key Pressed'

finally:
	camera.close()
	stream_pipe.stdin.close()
	stream_pipe.wait()
	print("Camera safely shut down")
	print("Good bye")

