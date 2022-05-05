from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from valorlib.Packets.DataStructures import WorldPosData
from ConditionEffect import *
from client import Client

import re
import time
import random

"""
This plugin essentially makes some of your shots hit very hard; up to 200x damage.
This does not work on piercing/multishot weapons. For example, it doesn't work on Staff of the Withering or any blade for the Blademaster.

requirements to use properly:
	- Do not use this plugin if your weapon is a piercing/multishot one.
	- Upon joining a new realm/dungeon, shoot one shot for the proxy to understand what weapon you are using.

NOTES: the server definitely checks these
- playershoot before enemyhit (tested)
	- the gap cannot be too big
- increasing bullet ID's (at least, non random forsure)
    - its also fine to have bulletID increasing by two
- time is also checked, you need to have sent the packets within a couple of seconds of the current time
"""

class DamageBoost(PluginInterface):

	"""
	Referring to Godmode.py: you can see both `hooks`, `load` and `defaultState` class variables have been instantiated.
	"""
	hooks = {PacketTypes.EnemyHit, PacketTypes.PlayerShoot, PacketTypes.Hello, PacketTypes.PlayerText}
	load = True
	defaultState = True

	lastEnemyHitSpam = 0
	multiplier = 5
	gap = 0
	internalBulletID = 0
	internalBulletTimeOffset = 0
	containerType = None

	def getAuthor(self):
		return "swrlly - https://github.com/swrlly"

	def onHello(self, client: Client, packet: Hello, send: bool) -> (Hello, bool):
		self.internalBulletID = 0
		self.internalBulletTimeOffset = 0
		self.containerType = None
		if client.currentMap == "Realm":
			self.multiplier = 5
		return (packet, send)

	def onPlayerShoot(self, client: Client, packet: PlayerShoot, send: bool) -> (PlayerShoot, bool):
		self.internalBulletID = (self.internalBulletID + 1) #% 128
		self.containerType = packet.containerType
		packet.bulletID = self.internalBulletID
		packet.time += self.internalBulletTimeOffset
		
		return (packet, send)

	def onEnemyHit(self, client: Client, packet: EnemyHit, send: bool) -> (EnemyHit, bool):

		if time.time() - self.lastEnemyHitSpam > 0.25:
			for i in range(1, self.multiplier + 1):
				p = PlayerShoot()
				p.time = packet.time + i * self.gap + self.internalBulletTimeOffset
				p.bulletID = self.internalBulletID
				p.pos = WorldPosData()
				p.pos.x = client.currentx
				p.pos.y = client.currenty
				p.containerType = self.containerType
				p.angle = 0.4943
				client.SendPacketToServer(CreatePacket(p))

				p = EnemyHit()
				p.time = packet.time + i * self.gap + self.internalBulletTimeOffset + random.randint(100, 200)
				p.bulletID = self.internalBulletID
				p.targetID = packet.targetID
				p.kill = False
				client.SendPacketToServer(CreatePacket(p))

				self.internalBulletID = (self.internalBulletID + 1) #% 128

			self.lastEnemyHitSpam = time.time()
			self.internalBulletTimeOffset += self.multiplier * self.gap

			return (packet, False)
		else:
			packet.bulletID = self.internalBulletID
			packet.time += self.internalBulletTimeOffset
			return (packet, send)


	# lots of custom commands
	def onPlayerText(self, client: Client, packet: PlayerText, send: bool) -> (PlayerText, bool):

		# we know we got a command
		if len(packet.text) > 0 and packet.text[0:3] == "/m ":
			try:		
				self.multiplier = int(packet.text.split(" ")[-1])
				client.createNotification("DamageBoost", "Set damage multiplier to {}".format(self.multiplier))
			except:
				client.createNotification("DamageBoost", "Incorrect syntax. Use '/m #' where # is a natural number.")
			send = False
		return (packet, send)
