from valorlib.Packets.Packet import *
from client import Client

class NoProjectile:

	hooks = {PacketTypes.EnemyShoot}
	load = True

	def onEnemyShoot(self, client: Client, packet: Packet, send: bool) -> (EnemyShoot, bool):
		return (packet, False)