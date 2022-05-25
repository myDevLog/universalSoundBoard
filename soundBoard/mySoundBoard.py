##libs for the gui
from tkinter import *
from tkinter import Tk, Button

##libs to get the sound-files
import os
from os import system
from pathlib import Path
from screeninfo import get_monitors

##lib to get commandline-args
import sys
from getopt import getopt, GetoptError

##to make sounds stop when wanted and to implement wanted behaviour for when the sound plays
import multiprocessing
from multiprocessing import Process, Value

import platform
from random import randint
from playsound import playsound





##encapsulates constants and important values for code quiality and integrity
class DataStorage():
	def __init__(self, path, padX=0, padY=0):
		self.__argErrorMsg = "Options:\n -h / --help\n -t / --text -> show the buttons with text\n -v / --volume = 0 <= x <= 100\n -a / --alignment = left, bottom, right"

		self.__backgroundColor = "#272727"
		self.__pad = (padX, padY)

		self.__windowAlignment = "bottom"
		self.__showButtonNames = False
		self.__volume = 80
		self.__processArgs()

		widthHeight = self.__getMonitorSpecs()
		self.__screenWidth = widthHeight[0]
		self.__screenHeight = widthHeight[1]


	def __processArgs(self):
		opts, args = self.__getArgs()
		
		##process the arguments
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print(self.__argErrorMsg)
				sys.exit(0)

			elif opt in ("-t", "--text"):
				self.__showButtonNames = True
			
			elif opt in ("-v", "--volume"):
				if not arg.isdigit():
					raise TypeError("The Argument of the option -v has to be of type Int")

				argAsInt = int(arg)
				if argAsInt not in range(0, 100):
					raise ValueError("The Argument of the option -v needs to be between 0 and 100")
				
				self.__volume = argAsInt

			elif opt in ("-a", "--alignment"):
				if arg in ("left", "bottom", "right"):
					self.__windowAlignment = arg
				else:
					raise ValueError("Argument of {0} has to be \"{1}\", \"{2}\" or \"{3}\"".format(opt, "left", "bottom", "right"))


	##made into its own function to make the code more readable 
	def __getArgs(self):
		##get arguments and check for errors 
		try:
			opts, args = getopt(sys.argv[1:], "htv:a:", ["help", "text", "volume=", "alignment="])
		except GetoptError:
			print(self.__argErrorMsg)
			sys.exit(2)

		return opts, args


	##return contents of specified path
	def getSoundDicts(self, path):
		##prevent crash due to wrong path
		if not os.path.isdir(path):
			raise ValueError("Can't read contents in getAllDicts(), directory {0} doesn’t exist".format(path))

		dirContents = os.listdir(path)

		directs = []
		for dirs in dirContents:
			if os.path.isdir(dirs):
				directs.append(dirs)

		##exit if no directory could be found
		if not directs:
			print("Error: No Sound-Directories found")
			sys.exit(2)

		return directs


	def __getMonitorSpecs(self):
		primaryMonitor = None

		##gets the monitor specs to place the board appropriately
		for monitor in get_monitors():
			if monitor.is_primary:
				primaryMonitor = monitor
				break

		return (primaryMonitor.width, primaryMonitor.height)


	##only getter, no setters to practically make them constants
	def getBackgroundColor(self):
		return self.__backgroundColor

	def getPadding(self):
		return self.__pad

	def getScreenWidth(self):
		return self.__screenWidth

	def getScreenHeight(self):
		return self.__screenHeight

	def getAlignment(self):
		return self.__windowAlignment

	def getButtonNameVis(self):
		return self.__showButtonNames

	def getVolume(self):
		return self.__volume





##responsible for playing and managing the soundfiles
class playSound:
	def __init__(self, playingVolume):
		self.__playingVolume = playingVolume

		self.__currentOS = platform.system()
		
		##to set the volume to its original value after playing the sound
		self.__prevVolume = self.__getVolume()

		self.__soundProcess = None
		##Value-type can be used across processes as a lock to coordinate them
		self.__soundIsPlaying = Value('b', False)


	def __setVolume(self, newVolume, unmuteSound):
		##to get OS-String uncomment:
		#print(platform.system())
				
		if self.__currentOS == "Linux":
			unmuteSound = "unmute" if unmuteSound else "mute"
			system("amixer -q -D pulse sset 'Master' {1} {0}%".format(newVolume, unmuteSound))
		
		elif self.__currentOS == "Darwin":
			#code Mac-Option to set the volume
			print("Volume couldn't get adjusted, setting the volume for MacOS is currently not implemented")
			pass
		
		elif self.__currentOS == "Windows":
			#code Windows-Option to set the volume
			print("Volume couldn't get adjusted, setting the volume for Windows is currently not implemented")
			pass
		
		else:
			raise Exception("No Operating System matches the cases in setVolume()")


	def __getVolume(self):
		if self.__currentOS == "Linux":
			return system("amixer get 'Master'")
		
		elif self.__currentOS == "Darwin":
			##code Mac-Option to get the volume
			pass
		
		elif self.__currentOS == "Windows":
			##code Windows-Option to get the volume
			pass
		
		else:
			raise Exception("No Operating System matches the cases in getVolume()")


	def __startSound(self, soundPath):
		self.__prevVolume = self.__getVolume()
		self.__setVolume(self.__playingVolume, True)

		playsound(soundPath)
		self.__soundIsPlaying.value = False
		
		self.__setVolume(self.__prevVolume, False)


	def playMySound(self, soundPath):
		if not self.__soundIsPlaying.value:
			self.__soundProcess = multiprocessing.Process(target=self.__startSound, args=(soundPath, ))
			self.__soundIsPlaying.value = True
			self.__soundProcess.start()
		else:
			self.__soundProcess.terminate()
			self.__soundIsPlaying.value = False
			self.__setVolume(self.__prevVolume, False)





class myButton(Button):
	def __init__(self, master, bgColor, pad, align, soundModule, button_text=None, path="./"):
		if not os.path.isfile(path + "unpressedButton.png") or not os.path.isfile(path + "pressedButton.png"):
			print("Directory {0} is missing at least one of the buttonImages".format(path))
			return;

		self.__unpressedButtonImage = PhotoImage(file=path + "unpressedButton.png")
		self.__pressedButtonImage = PhotoImage(file=path + "pressedButton.png")
		
		super().__init__(master)

		self.configure(image=self.__unpressedButtonImage)

		self.__soundFiles = self.__getSoundFiles(path)

		##dont create button if directory is empty
		if not self.__soundFiles:
			print("Error: No Sound-Files found in Directory {0}".format(path))
			return;

		self.__configure(bgColor, soundModule, path)

		if button_text != None:
			self.configure(text=button_text, foreground="White", activeforeground="White", font=("Ubuntu", 11))

		side = "left" if align in ("bottom") else "top"
		padX, padY = pad
		self.pack(side=side, padx=padX, pady=padY)
		self.__bind()


	def __configure(self, bgColor, soundModule, path):
		##disalbes background Button-Animation and Border
		self.configure(borderwidth=0, highlightthickness=0, relief=SUNKEN, background=bgColor, activebackground=bgColor)

		##image on top with text beneath it
		self.configure(compound="top")
		
		##needs to be a non class function without self and parameters		
		def playSound():
			soundIndex = randint(0, len(self.__soundFiles)-1)
			soundFile = self.__soundFiles[soundIndex]
			soundModule.playMySound(path + soundFile)

		self.configure(command=playSound)


	def __bind(self):
		##changes the sprite to pressed-button on press
		def onPress(event):
			caller = event.widget
			caller.configure(image=self.__pressedButtonImage)

		##changes the sprite to unpressed-button on press
		def onRelease(event):
			caller = event.widget
			caller.configure(image=self.__unpressedButtonImage)

		##change Button-sprite on press / release
		self.bind("<Button>", onPress)
		self.bind("<ButtonRelease>", onRelease)
		self.bind("<Leave>", onRelease)


	##return soundfiles of specified directory
	def __getSoundFiles(self, path):
		##prevent crash due to wrong path
		if not os.path.isdir(path):
			raise ValueError("Can't read contents in getSoundFile(), directory {0} doesn’t exist".format(path))

		dirContents = os.listdir(path)

		soundFiles = []

		for file in dirContents:
			if Path(file).suffix in [".mp3", ".wav"]:
				soundFiles.append(file)

		return soundFiles


	def __playSound(self):
		##play random file if more then one soundfile is present 
		soundIndex = randint(0, len(self.__soundFiles)-1)
		soundFile = self.__soundFiles[soundIndex]
		self.__soundModule.playMySound(self.path + soundFile)





##builds, draws the window and responsible for its logic
class soundBoard(Tk):
	def __init__(self, dicts, pad, bgColor, align, buttonNameVis, screenData, soundModule, title="My Sound-Board"):
		super().__init__()
		
		self.__soundModule = soundModule

		self.__configure(title, bgColor)
		self.__createList(bgColor, dicts, pad, align, buttonNameVis, screenData)
		self.__minimizeWindow(align, screenData)
		self.__centerWindow(align, screenData)
		

	def __configure(self, title, bgColor):
		self.title(title)
		self.configure(background=bgColor)
		self.resizable(True, True)
		self.attributes("-topmost", True)

		##sets the icon for the window
		pressedButton = PhotoImage(file="./soundBoardIcon.png", master=self)
		self.iconphoto(False, pressedButton)
		

	def __createList(self, bgColor, dicts, pad, align, buttonNameVis, screenData):
		##draw buttons inside canvas, so they can be moved via scrollbar
		self.canvas = Canvas(self, bg=bgColor)
		
		self.__createMasterFrame(bgColor, pad, align, dicts, buttonNameVis)
		self.__createScrollBar(align)

		self.canvas.create_window(0, 0, anchor='nw', window=self.masterFrame)

		self.canvas.update_idletasks()
		self.canvas.configure(width=self.masterFrame.winfo_width(), height=self.masterFrame.winfo_height())
		self.canvas.configure(background=bgColor, highlightthickness=0)
		
		if align in ("bottom"):
			self.canvas.configure(xscrollcommand=self.scrollbar.set)
		else:
			self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.canvas.configure(scrollregion=(self.canvas.bbox('all')))
		self.canvas.pack(fill="both", expand=True, side='top')


	def __createMasterFrame(self, bgColor, pad, align, dicts, buttonNameVis):
		self.masterFrame = Frame(self.canvas, bg=bgColor)
		
		for dirs in dicts:
			##show the text of the button
			myPath = "./{0}/".format(dirs)
			if buttonNameVis:
				myButton(self.masterFrame, bgColor, pad, align, self.__soundModule, dirs, myPath)
			##don't show the text of the button
			else:
				myButton(self.masterFrame, bgColor, pad, align, self.__soundModule, path=myPath)
			
		self.masterFrame.pack()


	def __createScrollBar(self, align):
		self.scrollbar = Scrollbar(self, orient=HORIZONTAL) if align in ("bottom") else Scrollbar(self, orient=VERTICAL)

		if align in ("bottom"):
			self.scrollbar.pack(fill="x", side=align)
			self.scrollbar.configure(command=self.canvas.xview)
		elif align in ("left", "right"):
			self.scrollbar.pack(fill="y", side=align)
			self.scrollbar.configure(command=self.canvas.yview)
		else:
			print("{0} isnt a to the program known alignment".format(align))
			sys.exit(2)


	##remove the scrollbar if not needed to save some space
	def __minimizeWindow(self, align, screenData):
		##unpack scrollbar if all butons fit on the screen
		self.masterFrame.update_idletasks()
		
		widthDif = self.masterFrame.winfo_width() - self.winfo_width()
		heightDif = self.masterFrame.winfo_height() - self.winfo_height()
		
		if self.masterFrame.winfo_width() + widthDif < screenData[0] and align in ("bottom"):
			self.scrollbar.pack_forget()
			self.canvas.update_idletasks()
		if self.masterFrame.winfo_height() + heightDif < screenData[1] and align in ("left", "right"):
			self.scrollbar.pack_forget()
			self.canvas.update_idletasks()


	def __centerWindow(self, align, screenData):
		self.update_idletasks()
		horizontalMiddle = (screenData[0] // 2) - (self.winfo_width() // 2)
		verticalMiddle = (screenData[1] // 2) - (self.winfo_height() // 2)
		if align == "bottom":
			super().geometry("+{0}+{1}".format(horizontalMiddle, screenData[1]))
		elif align == "left":
			super().geometry("+{0}+0".format(verticalMiddle))
		elif align == "right":
			super().geometry("+{0}+{1}".format(screenData[0], verticalMiddle))





myData = DataStorage(r"./", 2, 2)
soundModule = playSound(myData.getVolume())
screenData = (myData.getScreenWidth(), myData.getScreenHeight())
soundBoard(myData.getSoundDicts("./"), myData.getPadding(), myData.getBackgroundColor(), myData.getAlignment(), myData.getButtonNameVis(), screenData, soundModule).mainloop()