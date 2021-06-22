from valorlib.Packets.Packet import *
from ConditionEffect import *
from client import Client

"""
Stacks with speedy!
"""

class Swiftness:

	hooks = {PacketTypes.NewTick}
	load = True
	word = "Swiftness"

	def getAuthor(self):
		return "swrlly - https://github.com/swrlly"

	def onNewTick(self, client: Client, packet: NewTick, send: bool) -> (NewTick, bool):

		for obj in range(len(packet.statuses)):

			# got a packet that updates our stats
			if packet.statuses[obj].objectID == client.objectID:

				for s in range(len(packet.statuses[obj].stats)):
						
					if packet.statuses[obj].stats[s].statType == 96:
						packet.statuses[obj].stats[s].statValue |= effect1[self.word]
						break
				
				# if we didn't receive a packet that will update our stats, just add a new statdata object that does
				else:
					s = StatData()
					s.statType = 96
					s.statValue = client.effect1bits | effect1[self.word]
					# update the internal bit state to account for 1+ status effect mods
					client.effect1bits |= effect1[self.word]
					packet.statuses[obj].stats.append(s)
					break
				
			# else if the newtick doesn't modify our stats, create a new objectstatusdata that gives speedy
		else:
			o = ObjectStatusData()
			o.objectID = client.objectID
			# doesn't even matter if position isn't valid
			o.pos = WorldPosData()
			s = StatData()
			s.statType = 96
			s.statValue = client.effect1bits | effect1[self.word]
			client.effect1bits |= effect1[self.word]
			packet.statuses.append(o)

			

		return (packet, send)

	def shutdown(self, client: Client) -> None:

		packet2 = NewTick()
		packet2.tickID = 0
		packet2.tickTime = 0
		o = ObjectStatusData()
		o.objectID = client.objectID
		# doesn't even matter if position isn't valid
		o.pos = WorldPosData()
		s = StatData()
		s.statType = 96
		# remove speedy
		if client.effect1bits & effect1[self.word]:
			s.statValue = client.effect1bits - effect1[self.word]
			client.effect1bits -= effect1[self.word]
		else:
			s.statValue = client.effect1bits
		o.stats.append(s)
		packet2.statuses.append(o)
		packet2 = CreatePacket(packet2)
		client.SendPacketToClient(packet2)