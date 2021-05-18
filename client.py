import socket
import struct
import select
import time

from valorlib.Packets.Packet import *
from PluginManager import *
from RC4 import RC4

class Client:
	""" 
	This class holds data relevant to clients. 
	in here, we will also put the sockets. this allows the client class to send packets.
	from a design persepctive, this also makes sense since this can scale to clientless
	"""

	def __init__(self, pm: PluginManager):
		self.remoteHostAddr = "51.222.11.213"
		self.remoteHostPort = 2050
		self.objectID = None
		self.charID = None
		self.reconnecting = False
		self.connected = False
		self.clientSendKey = RC4(bytearray.fromhex("BA15DE"))
		self.clientReceiveKey = RC4(bytearray.fromhex("612a806cac78114ba5013cb531"))
		self.serverSendKey = RC4(bytearray.fromhex("612a806cac78114ba5013cb531"))
		self.serverReceiveKey = RC4(bytearray.fromhex("BA15DE"))
		self.gameSocket = None
		self.serverSocket = None
		self.pluginManager = pm
		self.currentMap = "None"
		self.gameIDs = {
			-1 : "Nexus",
			-2 : "Nexus",
			-5 : "Vault",
			-15 : "Marketplace",
			-16 : "Ascension Enclave",
			-17 : "Aspect Hall"
		}

		# stuff to ignore when debugging
		#self.ignoreIn = []
		#self.ignoreOut = []
		self.ignoreOut = [PacketTypes.Message, PacketTypes.Move, PacketTypes.Pong, PacketTypes.GotoAck, PacketTypes.PlayerShoot, PacketTypes.ShootAck]
		self.ignoreIn = [PacketTypes.Ping, PacketTypes.Goto, PacketTypes.Update, PacketTypes.NewTick]

		# client state syncs, these are public
		self.disableSpeedy = False
		self.disableInvulnerable = False
		self.disableSwiftness = False
		self.disableVengeance = False

		# containerType of the weapon you are using
		self.containerType = 0
		# first bullet time. allows server sync
		self.firstBulletTime = None
		# internal bullet ID to spoof packets
		self.internalBulletID = 0
		# last time enemies damaged themselves
		self.lastEnemySelfDamage = 0
		# last time you multiplied damage
		self.lastEnemyHitSpam = 0
		
		self.effect0bits = 0
		self.effect1bits = 0
		self.effect2bits = 0


		self.lastReconnect = 0
		self.lastReconKey = []
		self.lastGameID = 0
		self.useDisconnectedKey = None

	# disconnect the client from the proxy
	# disconnect the proxy from the server
	def Disconnect(self):
		self.connected = False
		if self.serverSocket:
			self.serverSocket.shutdown(socket.SHUT_RDWR)
			self.serverSocket.close()
		if self.gameSocket:
			self.gameSocket.shutdown(socket.SHUT_RDWR)
			self.gameSocket.close()
		self.gameSocket = None
		self.serverSocket = None

	# reset ciphers to default state
	def ResetCipher(self):
		self.clientSendKey.reset()
		self.clientReceiveKey.reset()
		self.serverSendKey.reset()
		self.serverReceiveKey.reset()

	# for now, we can just recon lazily
	def Reconnect(self):
		self.ConnectRemote(self.remoteHostAddr, self.remoteHostPort)
		self.connected = True

	# Connect to remote host. Block until client connected
	def ConnectRemote(self, host, port):
		# the invalid recon key bug is when client doesn't connect to the proxy server's socket
		# reduced sleep time and it seems to be ok now
		while self.gameSocket == None:
			time.sleep(0.005)

		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.connect((host, port))

	# closes both sockets
	def Close(self):
		self.gameSocket.close()
		self.serverSocket.close()

	# restart entire connection
	def reset(self):
		self.internalBulletID = 0
		self.firstBulletTime = None
		self.Disconnect()
		self.ResetCipher()
		self.Reconnect()

	# call this fcn when you reset connection
	def resetMapName(self):
		self.currentMap = "Nexus"

	"""
	Listens to packets from the client.
	"""
	def ListenToClient(self):

		header = self.gameSocket.recv(5)

		if len(header) == 0 or self.reconnecting:
			# try and fix this possible bug? why is the client sending nothing??
			# this only happens when you nexus
			# print("got length 0 packet from client")
			self.reset()
			return

		#while len(header) != 5:
		#	header += self.gameSocket.recv(5 - len(header))
		
		packetID = header[4]
		expectedPacketLength = struct.unpack("!i", header[:4])[0]

		# read the packet, subtract 5 cuz you already read header
		leftToRead = expectedPacketLength - 5
		data = bytearray()

		while (leftToRead > 0): 
			buf = bytearray(self.gameSocket.recv(leftToRead))
			data += buf
			leftToRead -= len(buf)

		# decipher it to update our internal state
		self.clientSendKey.decrypt(data)
		packet = Packet(header, data, packetID)		
		send = True

		"""
		# for debugging
		try:
			if packet.ID not in self.ignoreOut:
				print("Client sent:", PacketTypes.reverseDict[packet.ID])
		except:
			print("Got unknown packet from client")
		"""

		# hooks
		if packet.ID == PacketTypes.PlayerText:
			self.onPlayerText(packet)

		elif packet.ID == PacketTypes.Hello:
			# hello is always sent, try another map update name here
			p = Hello()
			p.read(packet.data)

			if p.gameID in self.gameIDs:
				self.currentMap = self.gameIDs[p.gameID]

		# plugin management
		elif packet.ID == PacketTypes.PlayerHit:
			packet, send = self.routePacket(packet, send, self.onPlayerHit)

		elif packet.ID == PacketTypes.GroundDamage:	
			packet, send = self.routePacket(packet, send, self.onGroundDamage)

		elif packet.ID == PacketTypes.EnemyHit:
			packet, send = self.routePacket(packet, send, self.onEnemyHit)

		elif packet.ID == PacketTypes.PlayerShoot:
			# make sure you're tracking the internal state
			# update the id now since this will percolate downstream to enemyhit
			self.internalBulletID = (self.internalBulletID + 1) % 128
			packet, send = self.routePacket(packet, send, self.onPlayerShoot)
			
			
		elif packet.ID == PacketTypes.OtherHit:
			# seems to help with the KA packet rejection rate
			# send = False
			pass

		if not send:
			return
		else:
			self.SendPacketToServer(packet)

	"""
	Listens to packets from the server.
	"""
	def ListenToServer(self):

		header = self.serverSocket.recv(5)

		if len(header) == 0 or self.reconnecting:
			# try and fix this possible bug? this happens every so often.
			# why this bug happens: client sends hello, but then server sends nothing.
			# doesn't matter if you keep trying to read bytes, server always sends nothing.
			# print("got 0 length packet from server")
			self.reset()
			return
			

		#while len(header) != 5:
		#	header += self.serverSocket.recv(5 - len(header))

		packetID = header[4]
		expectedPacketLength = struct.unpack("!i", header[:4])[0]
		# read the packet, subtract 5 cuz you already read header
		leftToRead = expectedPacketLength - 5
		data = bytearray()
		
		while (leftToRead > 0): 
			buf = bytearray(self.serverSocket.recv(leftToRead))
			data += buf
			leftToRead -= len(buf)

		# decipher it to update our internal state
		self.serverSendKey.decrypt(data)
		packet = Packet(header, data, packetID)
		send = True

		"""	
		# for debugging
		try:
			if packet.ID not in self.ignoreIn:
				print("Server sent:", PacketTypes.reverseDict[packet.ID])
		except:
			print("Got unknown packet from server, id", packet.ID)
		"""

		# hooks
		if packet.ID == PacketTypes.CreateSuccess:
			self.OnCreateSuccess(packet)

		elif packet.ID == PacketTypes.Reconnect:
			# update map name.
			p = Reconnect()
			p.read(packet.data)
			#p.PrintString()
			self.lastReconnect = time.time()
			self.lastGameID = p.gameID
			self.lastReconKey = p.key
			self.currentMap = p.name
			self.reconnecting = True

		# update internal effect state
		elif packet.ID == PacketTypes.NewTick:
			"""
			p = NewTick()
			p.read(packet.data)
			p.PrintString()
			for obj in range(len(p.statuses)):
				if p.statuses[obj].objectID != self.objectID:
					p.statuses[obj].PrintString()
					for s in range(len(p.statuses[obj].stats)):
						p.statuses[obj].stats[s].PrintString()
			"""
			packet, send = self.routePacket(packet, send, self.onNewTick)

		elif packet.ID == PacketTypes.EnemyShoot:
			packet, send = self.routePacket(packet, send, self.onEnemyShoot)

		elif packet.ID == PacketTypes.Failure:
			packet, send = self.routePacket(packet, send, self.onFailure)
			
		
		if send:
			self.SendPacketToClient(packet)

	"""
	Starts to listen for packets
	"""
	def Listen(self):

		while True:
			try:

				ready = select.select([self.gameSocket, self.serverSocket], [], [])[0]

				# prioritize reconnects
				if self.reconnecting:

					if self.gameSocket in ready:
						self.gameSocket.recv(50000)

					if self.serverSocket in ready:
						self.serverSocket.recv(50000)

					self.onReconnect()
					self.reconnecting = False
					return

				elif self.connected:
					
					# client has data ready to send to server
					if self.gameSocket in ready:
						self.ListenToClient()
					# server has data ready to send to client
					if self.serverSocket in ready:
						self.ListenToServer()

			except ConnectionAbortedError as e:
				print("Connection was aborted:", e)
				self.reset()
				self.resetMapName()

			except ConnectionResetError as e:
				print("Connection was reset")
				self.reset()
				self.resetMapName()

			except KeyboardInterrupt:
				print("User aborted. Shutting down proxy.")
				self.connected = False
				self.Close()
				return

			#except Exception as e:
			#	print("Something went terribly wrong.")
			#	print("Error:", e)
			#	print("Restarting...")
			#	self.reset()

	# activate godmode (actually not needed)
	def ActivateGodmode(self, packet) -> Packet:
		p = PlayerHit()
		p.read(packet.data)
		p.objectID = 0
		packet = CreatePacket(p)
		return packet


	"""

	Given a specific packet type, call the relevant client onPacketType function to read the packet
	Then, iterate through hook dict to call plugins which hook this packet.

	:param packet: A Packet object
	:param send: whether or not to send the packet
	:param onPacketType: The implemented callback inside a plugin when this packet type is encountered.
		This function will be defined within the Client class.

	returns: (Packet, send)
	"""
	def routePacket(self, packet: Packet, send, onPacketType) -> (Packet, bool):

		p = onPacketType(packet)
		#modified = False

		if packet.ID in self.pluginManager.hooks:
			for plugin in self.pluginManager.hooks[packet.ID]:
				# if the plugin is active
				if self.pluginManager.plugins[plugin]:
					# at each step, we are editing the packet on the wire
					# also make sure you're spelling your class methods correctly.
					p, send = getattr(plugin, "on" + PacketTypes.reverseDict[packet.ID])(self, p, send)
					modified = True

		# always create a new packet; this ensures our internal bullet ID state is synced
		# with our real shots
		#if modified:
		packet = CreatePacket(p)
		return (packet, send)


	# server -> client
	def SendPacketToClient(self, packet):
		self.clientReceiveKey.encrypt(packet.data)
		self.gameSocket.sendall(packet.format())

	# client -> server
	def SendPacketToServer(self, packet):
		self.serverReceiveKey.encrypt(packet.data)
		self.serverSocket.sendall(packet.format())

	# set objid to client's
	def OnCreateSuccess(self, packet):
		p = CreateSuccess()
		p.read(packet.data)
		self.objectID = p.objectID
		self.charID = p.charID	


##########################
# various necessary hooks
##########################

	def onFailure(self, packet: Packet) -> Failure:
		p = Failure()
		p.read(packet.data)
		#p.PrintString()
		return p

	def onPlayerHit(self, packet: Packet) -> PlayerHit:
		p = PlayerHit()
		p.read(packet.data)
		return p

	def onGroundDamage(self, packet: Packet) -> GroundDamage:
		p = GroundDamage()
		p.read(packet.data)
		return p

	def onEnemyShoot(self, packet: Packet) -> EnemyShoot:
		p = EnemyShoot()
		p.read(packet.data)
		return p

	def onEnemyHit(self, packet: Packet) -> EnemyHit:
		p = EnemyHit()
		p.read(packet.data)
		# since we have plugins that modify the bulletID, we need to make sure bulletID is synced as well
		#p.bulletID = self.internalBulletID
		return p

	def onPlayerShoot(self, packet: Packet) -> PlayerShoot:
		p = PlayerShoot()
		p.read(packet.data)
		self.containerType = p.containerType
		# to get bullet clock syncs, do int(time.time() * 1000 - self.firstBulletTime)
		# fix this later lmfao
		if self.firstBulletTime == None:
			self.firstBulletTime = time.time() * 1000 - p.time
		# this is causing bugs for multishot piercing weapons. ex: decimator goes from 0 -> 6 -> 12 every single playershoot
		#p.bulletID = self.internalBulletID
		return p

	def onNewTick(self, packet: Packet) -> NewTick:
		p = NewTick()
		p.read(packet.data)

		for obj in range(len(p.statuses)):
			# got a packet that updates our stats
			if p.statuses[obj].objectID == self.objectID:
				for s in range(len(p.statuses[obj].stats)):
					# 29, effect 0
					# 96, effect 1
					# 205, effect 2
					# armored, damaging serversided
						
					if p.statuses[obj].stats[s].statType == 29:
						self.effect0bits = p.statuses[obj].stats[s].statValue

					elif p.statuses[obj].stats[s].statType == 96:
						self.effect1bits = p.statuses[obj].stats[s].statValue

					elif p.statuses[obj].stats[s].statType == 205:
						self.effect2bits = p.statuses[obj].stats[s].statValue

		# now cover edge cases in plugins
		# pretty terrible engineering
		# this ensures our injected status effects are turned off and doesn't interfere with real speedy (like from warrior)
		self.turnOffInjectedStatuses()

		return p

	def turnOffInjectedStatuses(self):

		for plugin in self.pluginManager.plugins:
			if self.disableSpeedy and type(plugin).__name__ == "Speedy":
				plugin.shutdown(self)
				self.disableSpeedy = False

			elif self.disableSwiftness and type(plugin).__name__ == "Swiftness":
				plugin.shutdown(self)
				self.disableSwiftness = False

			elif self.disableInvulnerable and type(plugin).__name__ == "Invulnerable":
				plugin.shutdown(self)
				self.disableInvulnerable = False

			elif self.disableVengeance and type(plugin).__name__ == "Vengeance":
				plugin.shutdown(self)
				self.disableVengeance = False

	# playertext hook
	def onPlayerText(self, packet) -> None:
		p = PlayerText()
		p.read(packet.data)

		if p.text == "/dep":
			for i in range(0, 12):
				pp = PotionStorageInteraction()
				pp.type = i
				pp.action = 0
				self.SendPacketToServer(CreatePacket(pp))

		return p

	# when server sends reconnect
	def onReconnect(self):

		self.reset()