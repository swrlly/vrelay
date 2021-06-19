from valorlib.Packets.Packet import *
from client import Client

class AutoNexus:

	hooks = {PacketTypes.PlayerHit, PacketTypes.NewTick, PacketTypes.Hello}
	load = True
	threshold = 0.01
	internalHP = 999999
	internalHPChanged = False

	def onPlayerHit(self, client: Client, packet: PlayerHit, send: bool) -> (PlayerHit, bool):

		# everytime a player gets hit, check if the damage puts us under the threshold
		damage = client.seenProjectiles[packet.objectID][packet.bulletID].damage

		# put all damage in prot
		if client.currentProtection > 0:
			client.currentProtection = max(0, client.currentProtection - damage)

		# else no prot
		else:
			# first bullet after a new tick
			if self.internalHPChanged:
				self.internalHP = client.currentHP - damage
				self.internalHPChanged = False
			# 2+ bullets after new tick but before next new tick
			else:
				self.internalHP = self.internalHP - damage

        # finally, check if we need to nexus
		if client.currentProtection == 0 and self.internalHP < client.maxHP * self.threshold:
			client.FireNexusSignal()
			send = False

		return (packet, send)

	def onNewTick(self, client: Client, packet: NewTick, send: bool) -> (NewTick, bool):
		self.internalHPChanged = True
		self.internalHP = client.currentHP
		return (packet, send)




