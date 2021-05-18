from valorlib.Packets.Packet import *
from ConditionEffect import *
from client import Client

class NoDebuff:

	"""
	Need to research a bit more into blocking the effect entirely. Only removes after new tick happens; client is in control of the behavior of status effect.
	This means you need some type of dict that tells you each enemy's bullet IDs, then join bullet ID with object ID in update packet probably.
	Search XML's next
	"""

	hooks = {PacketTypes.NewTick}
	load = True
	effect0Remove = ["Quiet", "Hallucinating", "Weak", "Slowed", "Sick", "Stunned", "Blind", "Drunk", "Confused", "Paralyzed", "Stasis", "ArmorBroken", "Darkness", "Unstable", "Bleeding"]

	def onNewTick(self, client: Client, packet: NewTick, send: bool) -> (NewTick, bool):


		for obj in range(len(packet.statuses)):
			if packet.statuses[obj].objectID == client.objectID:
				for s in range(len(packet.statuses[obj].stats)):
					# if we got a packet representing us and a conditioneffect statdata
					if packet.statuses[obj].stats[s].statType == 29:
						# for each debuff
						for remove in self.effect0Remove:
							# if the bit is on
							if packet.statuses[obj].stats[s].statValue & (1 << self.getExponent(effect0[remove])):
								# remove the bit
								packet.statuses[obj].stats[s].statValue -= effect0[remove]
								# keep track of the state
								client.effect0bits -= effect0[remove]
						break
					# if we did not get a packet, just inject a new one without bad status effects
				else:
					s = StatData()
					s.statType = 29
					for remove in self.effect0Remove:
						if client.effect0bits  & (1 << self.getExponent(effect0[remove])):
							client.effect0bits -= effect0[remove]
					s.statValue = client.effect0bits
					packet.statuses[obj].stats.append(s)

		return (packet, send)
						
	# given a number of the form 2^k, k >= 1 returns k
	# if you give it a number x where 2^k <= x < 2^{k+1}, it will return k.
	def getExponent(self, num):
		cnt = 0
		while num != 1:
			num = num // 2
			cnt += 1
		return cnt