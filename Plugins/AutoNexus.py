from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from valorlib.Packets.DataStructures import WorldPosData
from ConditionEffect import *
from client import Client, AoEAutoException

import threading
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

# not used for now. thread must block to work
class AoEPredictionThread(threading.Thread):

	def run(self):

		self.exception = None

		try:
			self._target(*self._args)
			#self.predictAOE(*self._args)
		except AoEAutoException:
			self.exception = AoEAutoException

	def join(self):
		super(AoEPredictionThread, self).join()
		if self.exception:
			raise AoEAutoException

class AutoNexus(PluginInterface):

	"""
	Referring to Godmode.py: you can see both `hooks`, `load` and `defaultState` class variables have been instantiated.
	"""
	hooks = {PacketTypes.ShowEffect, PacketTypes.PlayerHit, PacketTypes.GroundDamage, PacketTypes.Hello, PacketTypes.NewTick, PacketTypes.PlayerText}
	load = True
	defaultState = False

	# here are some class variables that keep track of the internal state.
	effects = {
		1620: {
			'color': -65536,
			'radius' : 4,
			'damage' : 150,
			'time': 1.4
		}
	}
	lock = threading.Lock()
	internalHP = 0
	secondsBeforeLand = 0.25
	threshold = 0.05
	bulletsInTick = 0
	displayMessage = False

	def getAuthor(self) -> str:
		return "swrlly - https://github.com/swrlly"

	# what commands are in this plugin?
	def getCommands(self) -> list:
		return [
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

	def predictAOE(self, client: Client, enemy: int, timeOfEffect: int, pos: WorldPosData) -> None:

		while True:

			"""
			If aoe is about to land within the next tick, meaning even if you move out of range, send a Move packet,
			the server might not process it in time. Thus, you can still die even if you **are** out of range.
			Thus we subtract a small amount of time before landing to be able to predict right before death
			"""
			if time.time() - timeOfEffect >= self.effects[enemy]['time'] - self.secondsBeforeLand:
				# if we are in the circle of the AOE

				print("our hp is", self.internalHP)
				if client.inCircle(self.effects[enemy]['radius'], pos):

					self.bulletsInTick += 1

					# do damage calculation
					defense = client.defense
					damage = self.effects[enemy]['damage']

					# check if we are armoredt
					if client.effect0bits & effect0["Armored"]:
						defense *= 2
					# check if we are armor broken
					if client.effect0bits & effect0["ArmorBroken"]:
						defense = 0

					damage = int(max(damage - defense, damage * 0.25))

					# now calculate curse
					if client.effect1bits & effect1["Cursed"]:
						damage = int(damage * 1.3)

					self.lock.acquire(blocking = True)
					self.internalHP = self.internalHP - damage
					self.lock.release()

					print("our hp is now", self.internalHP)
					if self.internalHP < client.maxHP * self.threshold:
						self.displayMessage = True

						# if server is lagging, server might accept your nexus packet after AoE is applied.
						# solution: force dc client
						# client.FireNexusSignal()
						client.reconnecting = True
						client.connected = False
						client.reset()
				return
			time.sleep(0.005)


	def onShowEffect(self, client: Client, packet: ShowEffect, send: bool) -> (ShowEffect, bool):

		# if some object threw something
		if packet.effectType == 4:

			enemy = client.newObjects[packet.targetObjectID].objectType
			# if this throw is from an enemy we know about
			if enemy in self.effects:
				timeOfEffect = time.time()
				predictFutureThread = threading.Thread(target = self.predictAOE, args = (client, enemy, timeOfEffect, packet.pos1), daemon = True)
				predictFutureThread.start()
				print('thread started')

		return packet, send


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



