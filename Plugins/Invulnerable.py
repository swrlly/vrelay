from valorlib.Packets.Packet import *
from ConditionEffect import *
from client import Client

"""
this does not work. works for like one bullet or something
"""

class Invulnerable:

	hooks = {PacketTypes.NewTick}
	load = False

	def onNewTick(self, client: Client, packet: NewTick, send: bool) -> (NewTick, bool):

		for obj in range(len(packet.statuses)):

			# got a packet that updates our stats
			if packet.statuses[obj].objectID == client.objectID:

				for s in range(len(packet.statuses[obj].stats)):
						
					if packet.statuses[obj].stats[s].statType == 29:
						packet.statuses[obj].stats[s].statValue |= effect0['Invulnerable']
						break

				# if we didn't receive a packet that will update our stats, just add a new statdata object that does
				else:
					s = StatData()
					s.statType = 29
					s.statValue = client.effect0bits | effect0['Invulnerable']
					client.effect0bits |= effect0['Invulnerable']
					packet.statuses[obj].stats.append(s)
					break

			# else if the newtick doesn't modify our stats, create a new objectstatusdata that gives speedy
		else:
			o = ObjectStatusData()
			o.objectID = client.objectID
			# doesn't even matter if position isn't valid
			o.pos = WorldPosData()
			s = StatData()
			s.statType = 29
			s.statValue = client.effect0bits | effect0['Invulnerable']
			client.effect0bits |= effect0['Invulnerable']
			packet.statuses.append(o)
			

		return (packet, send)

	# here we also utilize packet injection to turn off the hack

	def shutdown(self, client: Client) -> None:

		packet2 = NewTick()
		packet2.tickID = 0
		packet2.tickTime = 0
		o = ObjectStatusData()
		o.objectID = client.objectID
		# doesn't even matter if position isn't valid
		o.pos = WorldPosData()
		s = StatData()
		s.statType = 29
		# remove speedy
		if client.effect1bits & effect0['Invulnerable']:
			s.statValue = client.effect0bits - effect0['Invulnerable']
		else:
			s.statValue = client.effect0bits
		o.stats.append(s)
		packet2.statuses.append(o)
		packet2 = CreatePacket(packet2)
		client.SendPacketToClient(packet2)