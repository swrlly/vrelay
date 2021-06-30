from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from ConditionEffect import *
from client import Client

import random
import math
import time

"""
This is a plugin that will automatically nexus for you when, upon taking damage, your HP falls below a certain threshold.
Current functionality:
- Able to predict future HP before the server updates.
- Compensates for server not having updated our real HP if server sends up it's idea of what our HP is.
- Does not account for AoE.

Hello Valor devs!
"""

class AutoNexus(PluginInterface):

	"""
	Referring to Godmode.py: you can see both `hooks`, `load` and `defaultState` class variables have been instantiated.
	"""
	hooks = {PacketTypes.PlayerHit, PacketTypes.GroundDamage, PacketTypes.Hello, PacketTypes.NewTick, PacketTypes.PlayerText}
	load = True
	defaultState = False

	# here are some class variables that keep track of the internal state.
	threshold = 0.05
	internalHP = 0
	internalHPChanged = False
	bulletsInTick = 0
	displayMessage = False

	def getAuthor(self) -> str:
		return "swrlly - https://github.com/swrlly"

	# what commands are in this plugin?
	def getCommands(self) -> list:
		return [
			'/an help - Syntax is `/an [number]` where number is between 0 and 99, inclusive.',
			'/an # - set nexus threshold to #, where # is an integer between 0 and 99, inclusive.'
		]

	# everytime a player gets hit, check if the damage puts us under the threshold
	def onPlayerHit(self, client: Client, packet: PlayerHit, send: bool) -> (PlayerHit, bool):

		if client.pluginManager.plugins[client.pluginManager.findClass("Godmode")]:
			return (packet, send)

		self.bulletsInTick += 1

		# get bullet damage from the packet.
		try:
			damage = client.seenProjectiles[packet.objectID][packet.bulletID].damage
		except KeyError as e:
			print("AutoNexus: Got error:", e)
			damage = 0
			
		# If user has protection, do not do any defense calculations.
			client.currentProtection = max(0, client.currentProtection - damage)

		# else no prot
		else:
			defense = client.defense

			# check if we are armored
			if client.effect0bits & effect0["Armored"]:
				defense *= 2

			# check if we are armor broken
			if client.effect0bits & effect0["ArmorBroken"]:
				defense = 0

			# check if bullet is armor piercing
			enemyObjectType = client.newObjects[packet.objectID].objectType
			bulletType = 0

			# weird bullet
			try:
				bulletType = client.seenProjectiles[packet.objectID][packet.bulletID].bulletType
			except KeyError as e:
				print("AutoNexus:", client.enemyName[enemyObjectType], "gave KeyError:", e)

			# if it is not armor piercing, do defense calculation
			if not client.bulletDictionary[(enemyObjectType, bulletType)]['armorPiercing']:
				damage = int(max(damage - defense, damage * 0.25))

			# now calculate curse
			if client.effect1bits & effect1["Cursed"]:
				damage = int(damage * 1.3)

			self.internalHP = self.internalHP - damage

		if self.internalHP < client.maxHP * self.threshold:
			self.displayMessage = True
			client.FireNexusSignal()
			return (packet, False)

		return (packet, send)

	# armor piercing
	# no clue if curse affects this
	def onGroundDamage(self, client: Client, packet: GroundDamage, send: bool) -> (GroundDamage, bool):

		self.bulletsInTick += 1

		if client.pluginManager.plugins[client.pluginManager.findClass("Godmode")]:
			return (packet, send)
		
		minDist = 9999999
		tileID = 0

		# first, get location of the tile from loaded in tiles
		# make sure it actually deals damage.
		for tile in client.newTiles:
			dist = math.sqrt((packet.pos.x - tile[0]) ** 2 + (packet.pos.y - tile[1]) ** 2)
			if dist <= minDist and client.tileDictionary[client.newTiles[tile]]["maxDamage"] > 0:
				tileID = client.newTiles[tile]
				minDist = dist
		
		# now that we have found the location of the tile, get it's groundtype and find max damage
		damage = client.tileDictionary[tileID]["maxDamage"]

		# now do same calculations as the bullets
		if client.currentProtection > 0:
			client.currentProtection = max(0, client.currentProtection - damage)

		# else no prot
		else:
			self.internalHP = self.internalHP - damage

		if self.internalHP < client.maxHP * self.threshold:
			self.displayMessage = True
			client.FireNexusSignal()
			return (packet, False)

		return (packet, send)

	def onHello(self, client: Client, packet: Hello, send: bool) -> (Hello, bool):

		if self.displayMessage:
			client.createNotification("AutoNexus",  "Saved at {} health".format(self.internalHP))
			self.displayMessage = False
		return (packet, send)


	def onNewTick(self, client: Client, packet: NewTick, send: bool) -> (NewTick, bool):

		# If server is possibly lagging in calculating all the playerHit's we sent it (meaning internalHP < clientHP)
		# The other inequality is also possible; however if internal < client then that means server has not processed all of our player hits yet.
		if self.bulletsInTick >= 1:
			self.internalHP = min(self.internalHP, client.currentHP)
		else:
			self.internalHP = client.currentHP	

		self.bulletsInTick = 0

		return (packet, send)

	# able to set the threshold with a command
	def onPlayerText(self, client: Client, packet: PlayerText, send: bool) -> (PlayerText, bool):

		if not client.screenshotMode and packet.text[:4] == "/an " or packet.text.strip() == "/an":
			try:
				command = packet.text.split(" ")[-1]
				if command == 'help':
					client.createNotification("AutoNexus", "Syntax is '/an [number]' where number is between 0 and 99, inclusive.")
					return (packet, False)
				else:
					test = int(command)
					if test < 0 or test >= 100:
						client.createNotification("AutoNexus", "Invalid setting; make sure you're inputting a number between 0 and 99, inclusive.")
						return (packet, False)

					self.threshold = test / 100
					client.createNotification("AutoNexus", "Set nexus threshold to {}%.".format(test))
					return (packet, False)
			except:
				client.createNotification("AutoNexus", "Invalid setting; make sure you're inputting a number between 0 and 99, inclusive.")
				return (packet, False)

		return (packet, send)

