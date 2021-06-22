# these imports are always necessary
from valorlib.Packets.Packet import *
from client import Client

# this is a short tutorial on how to write a plugin that will **only edit packets, not send new ones.**
# make sure the class name is capitalized, and matches the file's name.
class Godmode:

	"""
	for each plugin, you need to instantiate a *class variable* called hook.
	make sure this is a set.
	this will tell the program what packets you intend to hook
	why? suppose you have 10 plugins that utilize NewTick. You don't want to reread
	newtick 10 times. Also, you only want to call the plugins which contain a newtick
	hook. Remember, the faster this proxy is, the faster it can route packets.
	"""

	hooks = {PacketTypes.PlayerHit, PacketTypes.GroundDamage}

	# also, make sure you put this class variable to tell the PluginManager whether to load this plugin or not. If this is absent,
	# the manager will throw an exception.
	load = True

	"""
	Next, you need to write functions that will handle each packet type in your hooks.
	Make sure your function name is on + the capitalization found in PacketTypes.py, otherwise your function will not be called.
	This is all you need to write. Here is an example

	def onPacketType(self, client: Client, packet: Packet, send: bool)
		client is an instance of client
		packet is an instance of the specific packet type your function will handle. 
		send is whether or not this packet will be sent
		returns: (updated packet, send)
			send = true if you wish to send the packet, else false	

	Below is an example of these handlers. Since godmode is just blocking the packet, we can just set send to false

	"""

	def onPlayerHit(self, client: Client, packet: PlayerHit, send: bool) -> (PlayerHit, bool):
		return (packet, False)

	def onGroundDamage(self, client: Client, packet: GroundDamage, send: bool) -> (GroundDamage, bool):
		return (packet, False)

	def getAuthor(self):
		return "swrlly - https://github.com/swrlly"