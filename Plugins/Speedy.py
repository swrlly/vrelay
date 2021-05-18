from valorlib.Packets.Packet import *
from ConditionEffect import *
from client import Client

"""
here is a more involved situation where we edit the NewTick packet.
"""

class Speedy:

	hooks = {PacketTypes.NewTick}
	load = True

	def onNewTick(self, client: Client, packet: NewTick, send: bool) -> (NewTick, bool):

		for obj in range(len(packet.statuses)):

			# got a packet that updates our stats
			if packet.statuses[obj].objectID == client.objectID:

				for s in range(len(packet.statuses[obj].stats)):
						
					if packet.statuses[obj].stats[s].statType == 29:
						packet.statuses[obj].stats[s].statValue |= effect0['Speedy']
						break
				
				# if we didn't receive a packet that will update our stats, just add a new statdata object that does
				else:
					s = StatData()
					s.statType = 29
					s.statValue = client.effect0bits | effect0['Speedy']
					# update the internal bit state to account for 1+ status effect mods
					client.effect0bits |= effect0['Speedy']
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
			s.statValue = client.effect0bits | effect0['Speedy']
			client.effect0bits |= effect0['Speedy']
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
		s.statType = 29
		# remove speedy, this is why we keep the internal state
		if client.effect0bits & effect0['Speedy']:
			s.statValue = client.effect0bits - effect0['Speedy']
			client.effect0bits -= effect0['Speedy']
		else:
			s.statValue = client.effect0bits
		o.stats.append(s)
		packet2.statuses.append(o)
		packet2 = CreatePacket(packet2)
		client.SendPacketToClient(packet2)