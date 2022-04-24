from pynput.keyboard import Key
from pynput import keyboard

from playsound import playsound

import multiprocessing
from multiprocessing import Process, Value

#for windows use pycaw, 
import os
prevVolume = os.system("amixer get 'Master'")

import platform
currentOS = platform.system()



SOUND_VOLUME = 80
KEY_F1 = Key.f1
KEY_F2 = Key.f2
KEY_F3 = Key.f3
KEY_F4 = Key.f4
KEY_F5 = Key.f5
KEY_F6 = Key.f6
KEY_F7 = Key.f7
KEY_F8 = Key.f8
KEY_F9 = Key.f9
KEY_F10 = Key.f10
KEY_F11 = Key.f11
KEY_F12 = Key.f12



COMBINATIONS =[
	{KEY_F1},
	{KEY_F2},
	{KEY_F3},
	{KEY_F4}#,
	#{keyboard.Key.shift, keyboard.KeyCode(char='q')}
]



soundProcess = None
#Value can be used across processes to coordinate them
soundIsPlaying = Value('b', False)

current = set()





def setVolume(newVolume, unmuteSound):
	#to get OS-Name uncomment:
	#print(platform.system())
	
	global currentOS
	
	if currentOS == "Linux":
		unmuteSound = "unmute" if unmuteSound == True else "mute"
		os.system("amixer -D pulse sset 'Master' {1} {0}%".format(newVolume, unmuteSound))
	elif currentOS == "Darwin":
		#code Mac-Option to change the volume
		pass
	elif currentOS == "Windows":
		#code Windows-Option to change the volume
		pass
	else:
		raise Exception("No Operating System matches the cases in setVolume()")



def getVolume():
	global currentOS
	
	if currentOS == "Linux":
		return os.system("amixer get 'Master'")
	elif currentOS == "Darwin":
		#code Mac-Option to get the volume
		pass
	elif currentOS == "Windows":
		#code Windows-Option to get the volume
		pass
	else:
		raise Exception("No Operating System matches the cases in getVolume()")



def startSound(soundFile):
	global prevVolume
	prevVolume = getVolume()
	setVolume(SOUND_VOLUME, True)

	playsound(soundFile)
	global soundIsPlaying
	soundIsPlaying.value = False
	
	setVolume(prevVolume, False)


def execute(key):
	global soundIsPlaying
	global soundProcess

	if soundIsPlaying.value == False:
		arg = ""

		if key == KEY_F1:
			arg = "./JamesMaySaysWow.mp3"
		elif key == KEY_F2:
			arg = "./IlluminatiSoundEffect.mp3"
		if key == KEY_F3:
			arg = "./CricketsSoundEffect.mp3"
		elif key== KEY_F4:
			arg = "./BaDumTss.mp3"

		soundProcess = multiprocessing.Process(target=startSound, args=(arg,))
		soundIsPlaying.value = True
		soundProcess.start()
	else:
		soundProcess.terminate()
		soundIsPlaying.value = False
		setVolume(prevVolume, False)



def on_press(key):
	#uncomment following lines to get key-names and vk-Code (Virtual Key Code):
	#print("Key pressed: {0}".format(key))
	#print("vk-Code: " + str(key.value.vk))
	
	if any([key in COMBO for COMBO in COMBINATIONS]):		
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
			execute(key)



def on_release(key):
	if any([key in COMBO for COMBO in COMBINATIONS]):
		current.remove(key)



myListener = keyboard.Listener(
		on_press=on_press,
		on_release=on_release)
myListener.start()
myListener.join()
