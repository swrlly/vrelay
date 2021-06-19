import time
import sys

from tkinter import *
from PluginManager import *
from client import Client

class GUI:

	COLWIDTH = 20
	PADX = 10
	PADY = 5
	HEIGHT = 2
	RED = "#CF0029"
	GREEN = "#43810D"


	def __init__(self, pm: PluginManager, client: Client, proxy):

		# new gui
		self.pluginManager = pm
		self.client = client
		self.proxy = proxy
		self.root = Tk()
		self.root.geometry("460x220")
		self.root.resizable(False, False)
		self.root.title("vrelay by swrlly - for valor v3.2.4")

		self.buttonFrame = Frame(self.root)
		self.buttonFrame.grid(row = 0, column = 0)

		# godmode text
		self.godmodelabel = Label(self.buttonFrame, text = "Godmode", width = self.COLWIDTH, height = self.HEIGHT)
		self.godmodelabel.grid(row = 0, column = 0, padx = self.PADX, pady = self.PADY)

		# godmode button
		self.godmodetxt = StringVar()
		self.godmodetxt.set("OFF")
		self.godmodebtn = Button(self.buttonFrame, bd = 5, textvariable = self.godmodetxt, command = self.godmodeHandler, fg = self.RED)
		self.godmodebtn.grid(row = 0, column = 1, padx = self.PADX, pady = self.PADY)

		# noprojectile text
		self.noprojectilelabel = Label(self.buttonFrame, text = "Hide projectiles", width = self.COLWIDTH, height = self.HEIGHT)
		self.noprojectilelabel.grid(row = 1, column = 0, padx = self.PADX, pady = self.PADY)

		# noprojectile button
		self.noprojectiletxt = StringVar()
		self.noprojectiletxt.set("OFF")
		self.noprojectilebtn = Button(self.buttonFrame, bd = 5, textvariable = self.noprojectiletxt, command = self.noProjectileHandler, fg = self.RED)
		self.noprojectilebtn.grid(row = 1, column = 1, padx = self.PADX, pady = self.PADY)

		# speedy text
		self.speedylabel = Label(self.buttonFrame, text = "Speedy", width = self.COLWIDTH, height = self.HEIGHT)
		self.speedylabel.grid(row = 0, column = 2, padx = self.PADX, pady = self.PADY)

		# speedy button
		self.speedytxt = StringVar()
		self.speedytxt.set("OFF")
		self.speedybtn = Button(self.buttonFrame, bd = 5, textvariable = self.speedytxt, command = self.speedyHandler, fg = self.RED)
		self.speedybtn.grid(row = 0, column = 3, padx = self.PADX, pady = self.PADY)

		# swiftness text
		self.swiftnesslabel = Label(self.buttonFrame, text = "Swiftness", width = self.COLWIDTH, height = self.HEIGHT)
		self.swiftnesslabel.grid(row = 1, column = 2, padx = self.PADX, pady = self.PADY)

		# swiftness button
		self.swiftnesstxt = StringVar()
		self.swiftnesstxt.set("OFF")
		self.swiftnessbtn = Button(self.buttonFrame, bd = 5, textvariable = self.swiftnesstxt, command = self.swiftnessHandler, fg = self.RED)
		self.swiftnessbtn.grid(row = 1, column = 3, padx = self.PADX, pady = self.PADY)

		# nodebuff text
		self.nodebufflabel = Label(self.buttonFrame, text = "Remove client-side debuffs", width = self.COLWIDTH, height = self.HEIGHT)
		self.nodebufflabel.grid(row = 2, column = 0, padx = self.PADX, pady = self.PADY)

		# nodebuff button
		self.nodebufftxt = StringVar()
		self.nodebufftxt.set("OFF")
		self.nodebuffbtn = Button(self.buttonFrame, bd = 5, textvariable = self.nodebufftxt, command = self.noDebuffHandler, fg = self.RED)
		self.nodebuffbtn.grid(row = 2, column = 1, padx = self.PADX, pady = self.PADY)

		# an text
		self.anlabel = Label(self.buttonFrame, text = "Autonexus", width = self.COLWIDTH, height = self.HEIGHT)
		self.anlabel.grid(row = 2, column = 2, padx = self.PADX, pady = self.PADY)

		# an button
		self.antxt = StringVar()
		self.antxt.set("OFF")
		self.anbtn = Button(self.buttonFrame, bd = 5, textvariable = self.antxt, command = self.AutoNexusHandler, fg = self.RED)
		self.anbtn.grid(row = 2, column = 3, padx = self.PADX, pady = self.PADY)

		# realm text
		self.textFrame = Frame(self.root)
		self.textFrame.grid(row = 1, column = 0)

		self.shutdownbtn = Button(self.textFrame, bd = 5, text = "Shut down all plugins", command = self.shutdownHandler)
		self.shutdownbtn.grid(row = 0, column = 0, padx = 20, pady = 20)

		self.location = StringVar()
		self.location.set("Connected to {}!".format(client.currentMap))
		self.locationentry = Label(self.textFrame, bd = 1, textvariable = self.location)
		self.locationentry.grid(row = 0, column = 1, padx = 20, pady = 20)

	

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

	"""
		# restart text
		self.restartlabel = Label(text = "Restart Proxy", width = self.COLWIDTH, height = self.HEIGHT)
		self.restartlabel.grid(row = 2, column = 0, padx = self.PADX, pady = self.PADY)

		# restart button
		self.restartlabeltxt = StringVar()
		self.restartlabeltxt.set("Restart")
		self.restartbtn = Button(self.root, bd = 5, textvariable = self.restartlabeltxt, command = self.restartHandler)
		self.restartbtn.grid(row = 2, column = 1, padx = self.PADX, pady = self.PADY)
	"""

		
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

	"""
	# when user wishes to restart
	def restartHandler(self):
		# break out of Listen thread
		self.proxy.Restart()
	"""

	# returns relevant class you searched for
	def findClass(self, text: str):
		for plugin in self.pluginManager.plugins:
			if type(plugin).__name__ == text:
				return plugin
			
	def start(self):
		while True:
			#self.root.update_idletasks()
			try:
				self.root.update()
				self.location.set("Connected to {}!".format(self.client.currentMap))
			except KeyboardInterrupt:
				return
			except TclError:
				print("Closed GUI. Shutting down proxy.")
				return
			time.sleep(0.005)
		



	