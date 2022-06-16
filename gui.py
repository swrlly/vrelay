import time
import sys
import ctypes
import webbrowser

from tkinter import *
from tkinter import font
from PluginManager import *
from client import Client

# declare exported functions from user32
GetForegroundWindow = ctypes.WinDLL('User32').GetForegroundWindow
GetForegroundWindow.restype = ctypes.c_void_p

GetWindowTextW = ctypes.WinDLL('User32').GetWindowTextW
GetWindowTextW.argtype = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
GetWindowTextW.restype = ctypes.c_int

# capture keypresses
GetAsyncKeyState = ctypes.WinDLL('User32').GetAsyncKeyState
GetAsyncKeyState.argtype = [ctypes.c_int]
GetAsyncKeyState.restype = ctypes.c_short

# 1 - 9 is just ZERO + number offset
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
SPACE = 0x20
ZERO = 0x30
ESC = 0x1B
F1 = 0x70
F2 = 0x71
F3 = 0x72
F4 = 0x73
F5 = 0x74
F6 = 0x75
F7 = 0x76
globalFont = "Microsoft JhengHei UI"


class GUI:

	HEIGHT = 2
	BTNWIDTH = 4
	BUTTONDEPTH = 2
	ROWSPACE = 40
	KEYYSPACE = 10
	BUTTONYSPACE = 6
	# red but like "off"
	#RED = "#CF0029"
	RED = "#919191"
	#GREEN = "#43810D"
	GREEN = "#EEA1F5"
	WHITE = "#FFFFFF"
	BLACK = "#000000"
	TEXTCOL = '#C5C5C5'

	#def placeLabel()

	def subimage(self, label, src, left, top, right, bottom):
		# keep a reference to the background image, otherwise will display white box
		dst = PhotoImage()
		self.images.append(dst)
		# copy background image to size of box our label takes up
		dst.tk.call(dst, 'copy', src, '-from',
					left, top, right, bottom, '-to', 0, 0)
		# update our label with the background image
		label.configure(image = dst, compound = 'center', height = label.winfo_reqheight() - 4, width = label.winfo_reqwidth() - 4)

	def __init__(self, pm: PluginManager, client: Client, proxy):

		# new gui
		self.pluginManager = pm
		self.client = client
		self.proxy = proxy
		self.images = []

		# calibri meh but works
		# @Microsoft YaHei UI ok as well
		self.root = Tk()
		self.sizex = 350
		self.sizey = 430
		self.root.geometry("{}x{}".format(self.sizex, self.sizey))
		self.root.resizable(False, False)
		self.root.title("vrelay")

		self.useChallengeLeague = False
		self.featureFont = font.Font(family = globalFont, weight = "bold", size = 15)
		self.keyFont = font.Font(family = globalFont, weight = "bold", size = 8)
		self.btnFont = font.Font(family = globalFont, weight = "bold", size = 15)
		# custom background
		self.bg = PhotoImage(file = "images/black.png")
		#self.canvas = Label(self.root, image = self.bg)
		#self.canvas.place(x=-2, y=-2)

		# canvas to draw lines
		self.drawingPad = Canvas(self.root, bd = 0, relief='ridge', highlightthickness = 0)
		self.drawingPad.create_image(0, 0, anchor = NW, image = self.bg)
		self.drawingPad.pack(fill=BOTH, expand=1)

		x, y = 15, 5
		self.vrelayLabel = Label(bd = 0, text = "vrelay", fg = 'white', cursor = "hand2")
		self.vrelayLabel['font'] = font.Font(family = globalFont, weight = "bold", size = 30)
		self.subimage(self.vrelayLabel, self.bg, x - 2, y - 2, x + self.vrelayLabel.winfo_reqwidth(), y + self.vrelayLabel.winfo_reqheight())
		self.vrelayLabel.place(x = x, y = y)
		self.vrelayLabel.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/swrlly/vrelay"))

		"""
		x, y = 259, self.sizey - 25
		self.challengetxt = StringVar()
		self.challengetxt.set("Normal Server")
		self.challengebtn = Button(bd = 0, textvariable = self.challengetxt, command = self.challengeHandler, width = 12, fg = self.RED)
		self.challengebtn['font'] = self.keyFont#font.Font(family = globalFont, weight = "bold", size = 8)
		self.subimage(self.challengebtn, self.bg, x - 2, y - 2, x + self.challengebtn.winfo_reqwidth(), y + self.challengebtn.winfo_reqheight())
		self.challengebtn.place(x = x, y = y)
		"""

		x, y = 134, 32
		self.version = Label(bd = 0, text = 'v3.3.4', bg = 'black', fg = self.TEXTCOL)
		self.version['font'] = self.keyFont
		self.subimage(self.version, self.bg, x - 2, y - 2, x + self.version.winfo_reqwidth(), y + self.version.winfo_reqheight())
		self.version.place(x = x, y = y)

		x, y = 15, 55
		self.author = Label(bd = 0, text = "by swrlly", fg = '#99CCFF', cursor="hand2")
		self.author['font'] = font.Font(family = globalFont, size = 14)
		self.subimage(self.author, self.bg, x - 2, y - 2, x + self.author.winfo_reqwidth(), y + self.author.winfo_reqheight())
		self.author.place(x = x, y = y)
		self.author.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/swrlly"))

		#################################
		# an text
		# this is where we start y offsets
		x, y = 45, 105
		self.anlabel = Label(bd = 0, text = "Autonexus", fg = self.TEXTCOL)
		self.anlabel['font'] = self.featureFont
		self.subimage(self.anlabel, self.bg, x - 2, y - 2, x + self.anlabel.winfo_reqwidth(), y + self.anlabel.winfo_reqheight())
		self.anlabel.place(x = x, y = y)

		# an key text
		x, ytmp = 210, y + self.KEYYSPACE
		self.ankeylabel = Label(bd = 0, text = "F1", fg = self.TEXTCOL)
		self.ankeylabel['font'] = self.keyFont
		self.subimage(self.ankeylabel, self.bg, x - 2, ytmp - 2, x + self.ankeylabel.winfo_reqwidth(), ytmp + self.ankeylabel.winfo_reqheight())
		self.ankeylabel.place(x = x, y = ytmp)

		# an button
		x, ytmp = 260, y - self.BUTTONYSPACE
		self.antxt = StringVar()
		self.antxt.set("OFF")
		self.anbtn = Button(bd = 0, textvariable = self.antxt, command = self.AutoNexusHandler, width = self.BTNWIDTH, fg = self.RED)
		self.anbtn['font'] = self.btnFont
		self.subimage(self.anbtn, self.bg, x - 2, ytmp - 2, x + self.anbtn.winfo_reqwidth(), ytmp + self.anbtn.winfo_reqheight())
		self.anbtn.place(x = x, y = ytmp)

		#################################	
		# godmode text
		x, y = 45, y + self.ROWSPACE
		self.godmodelabel = Label(bd = 0, text = "Godmode", fg = self.TEXTCOL)
		self.godmodelabel['font'] = self.featureFont
		self.subimage(self.godmodelabel, self.bg, x - 2, y - 2, x + self.godmodelabel.winfo_reqwidth(), y + self.godmodelabel.winfo_reqheight())
		self.godmodelabel.place(x = x, y = y)

		# godmode key text
		x, ytmp = 210, y + self.KEYYSPACE
		self.gmkeylabel = Label(bd = 0, text = "F2", fg = self.TEXTCOL)
		self.gmkeylabel['font'] = self.keyFont
		self.subimage(self.gmkeylabel, self.bg, x - 2, ytmp - 2, x + self.gmkeylabel.winfo_reqwidth(), ytmp + self.gmkeylabel.winfo_reqheight())
		self.gmkeylabel.place(x = x, y = ytmp)

		# godmode button
		x, ytmp = 260, y - self.BUTTONYSPACE
		self.godmodetxt = StringVar()
		self.godmodetxt.set("OFF")
		self.godmodebtn = Button(bd = 0, textvariable = self.godmodetxt, command = self.godmodeHandler, width = self.BTNWIDTH, fg = self.RED)
		self.godmodebtn['font'] = self.btnFont
		self.subimage(self.godmodebtn, self.bg, x - 2, ytmp - 2, x + self.godmodebtn.winfo_reqwidth(), ytmp + self.godmodebtn.winfo_reqheight())
		self.godmodebtn.place(x = x, y = ytmp)

		#################################	
		# no proj text
		x, y = 45, y + self.ROWSPACE
		self.noprojectilelabel = Label(bd = 0, text = "No Projectile", fg = self.TEXTCOL)
		self.noprojectilelabel['font'] = self.featureFont
		self.subimage(self.noprojectilelabel, self.bg, x - 2, y - 2, x + self.noprojectilelabel.winfo_reqwidth(), y + self.noprojectilelabel.winfo_reqheight())
		self.noprojectilelabel.place(x = x, y = y)

		# no proj text key text
		x, ytmp = 210, y + self.KEYYSPACE
		self.npkeylabel = Label(bd = 0, text = "F3", fg = self.TEXTCOL)
		self.npkeylabel['font'] = self.keyFont
		self.subimage(self.npkeylabel, self.bg, x - 2, ytmp - 2, x + self.npkeylabel.winfo_reqwidth(), ytmp + self.npkeylabel.winfo_reqheight())
		self.npkeylabel.place(x = x, y = ytmp)

		# no proj button
		x, ytmp = 260, y - self.BUTTONYSPACE
		self.noprojectiletxt = StringVar()
		self.noprojectiletxt.set("OFF")
		self.noprojectilebtn = Button(bd = 0, textvariable = self.noprojectiletxt, command = self.noProjectileHandler, width = self.BTNWIDTH, fg = self.RED)
		self.noprojectilebtn['font'] = self.btnFont
		self.subimage(self.noprojectilebtn, self.bg, x - 2, ytmp - 2, x + self.noprojectilebtn.winfo_reqwidth(), ytmp + self.noprojectilebtn.winfo_reqheight())
		self.noprojectilebtn.place(x = x, y = ytmp)

		###################################
		# y is 205 now
		y += 46
		# draw a line with +46 gap from noprojectile y
		# the text was 25 high, so essentially this is 25 down from No Projectile. Thus, next gap must be 21 down as well
		self.drawingPad.create_line(45, y, 305, y, dash=(1, 5), fill = self.TEXTCOL)

		###################################
		# speedy text
		x, y = 45, y + 21
		self.speedylabel = Label(bd = 0, text = "Speedy", fg = self.TEXTCOL)
		self.speedylabel['font'] = self.featureFont
		self.subimage(self.speedylabel, self.bg, x - 2, y - 2, x + self.speedylabel.winfo_reqwidth(), y + self.speedylabel.winfo_reqheight())
		self.speedylabel.place(x = x, y = y)

		# speedy text key text
		x, ytmp = 210, y + self.KEYYSPACE
		self.spdkeylabel = Label(bd = 0, text = "F4", fg = self.TEXTCOL)
		self.spdkeylabel['font'] = self.keyFont
		self.subimage(self.spdkeylabel, self.bg, x - 2, ytmp - 2, x + self.spdkeylabel.winfo_reqwidth(), ytmp + self.spdkeylabel.winfo_reqheight())
		self.spdkeylabel.place(x = x, y = ytmp)

		# speedy button
		x, ytmp = 260, y - self.BUTTONYSPACE
		self.speedytxt = StringVar()
		self.speedytxt.set("OFF")
		self.speedybtn = Button(bd = 0, textvariable = self.speedytxt, command = self.speedyHandler, width = self.BTNWIDTH, fg = self.RED)
		self.speedybtn['font'] = self.btnFont
		self.subimage(self.speedybtn, self.bg, x - 2, ytmp - 2, x + self.speedybtn.winfo_reqwidth(), ytmp + self.speedybtn.winfo_reqheight())
		self.speedybtn.place(x = x, y = ytmp)

		###################################
		# swiftness text
		x, y = 45, y + self.ROWSPACE
		self.swiftnesslabel = Label(bd = 0, text = "Swiftness", fg = self.TEXTCOL)
		self.swiftnesslabel['font'] = self.featureFont
		self.subimage(self.swiftnesslabel, self.bg, x - 2, y - 2, x + self.swiftnesslabel.winfo_reqwidth(), y + self.swiftnesslabel.winfo_reqheight())
		self.swiftnesslabel.place(x = x, y = y)

		# swiftness key text
		x, ytmp = 210, y + self.KEYYSPACE
		self.swiftkeylabel = Label(bd = 0, text = "F5", fg = self.TEXTCOL)
		self.swiftkeylabel['font'] = self.keyFont
		self.subimage(self.swiftkeylabel, self.bg, x - 2, ytmp - 2, x + self.swiftkeylabel.winfo_reqwidth(), ytmp + self.swiftkeylabel.winfo_reqheight())
		self.swiftkeylabel.place(x = x, y = ytmp)

		# swiftness button
		x, ytmp = 260, y - self.BUTTONYSPACE
		self.swiftnesstxt = StringVar()
		self.swiftnesstxt.set("OFF")
		self.swiftnessbtn = Button(bd = 0, textvariable = self.swiftnesstxt, command = self.swiftnessHandler, width = self.BTNWIDTH, fg = self.RED)
		self.swiftnessbtn['font'] = self.btnFont
		self.subimage(self.swiftnessbtn, self.bg, x - 2, ytmp - 2, x + self.swiftnessbtn.winfo_reqwidth(), ytmp + self.swiftnessbtn.winfo_reqheight())
		self.swiftnessbtn.place(x = x, y = ytmp)

		###################################
		# nodebuff text
		x, y = 45, y + self.ROWSPACE
		self.nodebufflabel = Label(bd = 0, text = "Ignore Debuff", fg = self.TEXTCOL)
		self.nodebufflabel['font'] = self.featureFont
		self.subimage(self.nodebufflabel, self.bg, x - 2, y - 2, x + self.nodebufflabel.winfo_reqwidth(), y + self.nodebufflabel.winfo_reqheight())
		self.nodebufflabel.place(x = x, y = y)

		# nodebuff key text
		x, ytmp = 210, y + self.KEYYSPACE
		self.ndbkeylabel = Label(bd = 0, text = "F6", fg = self.TEXTCOL)
		self.ndbkeylabel['font'] = self.keyFont
		self.subimage(self.ndbkeylabel, self.bg, x - 2, ytmp - 2, x + self.ndbkeylabel.winfo_reqwidth(), ytmp + self.ndbkeylabel.winfo_reqheight())
		self.ndbkeylabel.place(x = x, y = ytmp)

		# nodebuff button
		x, ytmp = 260, y - self.BUTTONYSPACE
		self.nodebufftxt = StringVar()
		self.nodebufftxt.set("OFF")
		self.nodebuffbtn = Button(bd = 0, textvariable = self.nodebufftxt, command = self.noDebuffHandler, width = self.BTNWIDTH, fg = self.RED)
		self.nodebuffbtn['font'] = self.btnFont
		self.subimage(self.nodebuffbtn, self.bg, x - 2, ytmp - 2, x + self.nodebuffbtn.winfo_reqwidth(), ytmp + self.nodebuffbtn.winfo_reqheight())
		self.nodebuffbtn.place(x = x, y = ytmp)
		
		x, y = 5, self.sizey - 23
		self.location = StringVar()
		self.location.set("Connected to {}!".format(client.currentMap))
		self.locationentry = Label(bd = 0, textvariable = self.location, bg = 'black', fg = self.RED)
		self.locationentry['font'] = self.keyFont
		#self.subimage(self.locationentry, self.bg, x - 2, y - 2, x + self.locationentry.winfo_reqwidth(), y + self.locationentry.winfo_reqheight())
		self.locationentry.place(x = x, y = y)

	def challengeHandler(self):

		# change to normal
		if not self.useChallengeLeague:
			self.challengetxt.set("Challenge Server")
			self.client.remoteHostAddr = "103.195.100.203"
		else:
			self.challengetxt.set("Normal Server")
			self.client.remoteHostAddr = "51.222.11.213"

		self.useChallengeLeague = not self.useChallengeLeague

	def shutdownHandler(self):

		# turn off hooks
		for plugin in self.pluginManager.plugins:
			self.pluginManager.plugins[plugin] = False

		# change UI
		self.godmodetxt.set("OFF")
		self.godmodebtn.config(fg = self.RED)
		self.noprojectiletxt.set("OFF")
		self.noprojectilebtn.config(fg = self.RED)
		self.antxt.set("OFF")
		self.anbtn.config(fg = self.RED)
		self.speedytxt.set("OFF")
		self.speedybtn.config(fg = self.RED)
		self.swiftnesstxt.set("OFF")
		self.swiftnessbtn.config(fg = self.RED)
		self.nodebufftxt.set("OFF")
		self.nodebuffbtn.config(fg = self.RED)

		# next new tick packet will actually send shutdown packet
		self.client.disableSpeedy = True
		self.client.disableSwiftness = True
		
	# when the button is clicked
	def godmodeHandler(self):
		if self.pluginManager.plugins[self.findClass("Godmode")]:
			self.pluginManager.plugins[self.findClass("Godmode")] = False
			self.godmodetxt.set("OFF")
			self.godmodebtn.config(fg = self.RED)
		else:
			self.pluginManager.plugins[self.findClass("Godmode")] = True
			self.godmodetxt.set("ON")
			self.godmodebtn.config(fg = self.GREEN)

	# when the button is clicked
	def noDebuffHandler(self):
		if self.pluginManager.plugins[self.findClass("NoDebuff")]:
			self.pluginManager.plugins[self.findClass("NoDebuff")] = False
			self.nodebufftxt.set("OFF")
			self.nodebuffbtn.config(fg = self.RED)
		else:
			self.pluginManager.plugins[self.findClass("NoDebuff")] = True
			self.nodebufftxt.set("ON")
			self.nodebuffbtn.config(fg = self.GREEN)

	# when the button is clicked
	def noProjectileHandler(self):
		if self.pluginManager.plugins[self.findClass("NoProjectile")]:
			self.pluginManager.plugins[self.findClass("NoProjectile")] = False
			self.noprojectiletxt.set("OFF")
			self.noprojectilebtn.config(fg = self.RED)
		else:
			self.pluginManager.plugins[self.findClass("NoProjectile")] = True
			self.noprojectiletxt.set("ON")
			self.noprojectilebtn.config(fg = self.GREEN)

	# when the button is clicked
	def speedyHandler(self):
		if self.pluginManager.plugins[self.findClass("Speedy")]:
			self.client.disableSpeedy = True
			self.pluginManager.plugins[self.findClass("Speedy")] = False
			self.speedytxt.set("OFF")
			self.speedybtn.config(fg = self.RED)
		else:
			self.client.disableSpeedy = False
			self.pluginManager.plugins[self.findClass("Speedy")] = True
			self.speedytxt.set("ON")
			self.speedybtn.config(fg = self.GREEN)	

	# when the button is clicked
	def AutoNexusHandler(self):
		if self.pluginManager.plugins[self.findClass("AutoNexus")]:
			self.pluginManager.plugins[self.findClass("AutoNexus")] = False
			self.antxt.set("OFF")
			self.anbtn.config(fg = self.RED)
		else:
			self.pluginManager.plugins[self.findClass("AutoNexus")] = True
			self.antxt.set("ON")
			self.anbtn.config(fg = self.GREEN)

	# when the button is clicked
	def swiftnessHandler(self):
		if self.pluginManager.plugins[self.findClass("Swiftness")]:
			self.client.disableSwiftness = True
			self.pluginManager.plugins[self.findClass("Swiftness")] = False
			self.swiftnesstxt.set("OFF")
			self.swiftnessbtn.config(fg = self.RED)
		else:
			self.client.disableSwiftness = False
			self.pluginManager.plugins[self.findClass("Swiftness")] = True
			self.swiftnesstxt.set("ON")
			self.swiftnessbtn.config(fg = self.GREEN)	

	# returns relevant class you searched for
	def findClass(self, text: str):
		for plugin in self.pluginManager.plugins:
			if type(plugin).__name__ == text:
				return plugin
			
	def start(self):

		buf = ctypes.create_unicode_buffer(50)

		while True:
			#self.root.update_idletasks()
			try:
				
				GetWindowTextW(GetForegroundWindow(), buf, 50)
				self.root.update()
				self.location.set("Connected to {}!".format(self.client.currentMap))

				# check valor last, key press down is rare event
				if GetAsyncKeyState(F1) & 1 and buf.value == "Valor":
					self.AutoNexusHandler()
				elif GetAsyncKeyState(F2) & 1 and buf.value == "Valor":
					self.godmodeHandler()
				elif GetAsyncKeyState(F3) & 1 and buf.value == "Valor":
					self.noProjectileHandler()
				elif GetAsyncKeyState(F4) & 1 and buf.value == "Valor":
					self.speedyHandler()
				elif GetAsyncKeyState(F5) & 1 and buf.value == "Valor":
					self.swiftnessHandler()
				elif GetAsyncKeyState(F6) & 1 and buf.value == "Valor":
					self.noDebuffHandler()
				elif GetAsyncKeyState(ESC) & 1 and buf.value == "Valor":
					self.shutdownHandler()
					
			except KeyboardInterrupt:
				return
			except TclError:
				print("Closed GUI. Shutting down proxy.")
				return
			time.sleep(0.005)
