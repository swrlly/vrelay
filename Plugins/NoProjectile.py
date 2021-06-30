from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from client import Client

class NoProjectile(PluginInterface):

	hooks = {PacketTypes.EnemyShoot}
	load = True
	defaultState = False

	def getAuthor(self) -> str:
		return "swrlly - https://github.com/swrlly"

	def onEnemyShoot(self, client: Client, packet: Packet, send: bool) -> (EnemyShoot, bool):
		return (packet, False)