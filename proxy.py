import threading
import pickle
import sys

from Logger import Logger
from client import *
from PluginManager import *
from gui import GUI


DEBUG_LENGTH = 10
DEBUG = True


class Proxy:

	def __init__(self, pm: PluginManager, client: Client):

		self.localHostAddr = "127.0.0.1"
		self.localHostPort = 2050 # look up 843 and flash
		self.managerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.pluginManager = pm
		self.client = client

		self.active = False
		self.serverMonitorThread = None

	"""
	the purpose of this function is to allow client -> proxy then server -> proxy reconnects.
	it's in a thread to "monitor" when our client requires a new socket to the proxy
	in a sense, it is the server socket.
	"""
	def ServerMonitor(self):
		self.managerSocket.bind((self.localHostAddr, self.localHostPort))
		self.managerSocket.listen(3)
		# always listening for client connect
		while True:
			self.client.gameSocket, addr = self.managerSocket.accept()
			#print("new client")

	def Start(self):
		self.active = True
		# start up server socket
		self.serverMonitorThread = threading.Thread(target = self.ServerMonitor, daemon = True)
		self.serverMonitorThread.start()
		self.Connect()

	def Connect(self):
		# connect sockets first
		self.client.ConnectRemote(self.client.remoteHostAddr, self.client.remoteHostPort)
		self.client.connected = True

		# listen for packets
		while True:
			self.client.Listen()

	"""
	def Restart(self):
		self.client.Disconnect()
		self.client.ResetCipher()
		threading.Thread(target = self.Connect, daemon = False).start()
	"""
					
def main():
	print("[Initializer]: Loading plugins...")
	plugins = PluginManager()
	if not plugins.initialize():
		print("Shutting down.")
		return

	print("[Initializer]: Deserializing objects...")
	with open("bin/BulletDictionary.pkl", "rb") as f:
		bulletDictionary = pickle.load(f)
		print("[Initializer]: Deserialized {} enemies.".format(len(set([x[0] for x in bulletDictionary.keys()]))))            
		print("[Initializer]: Deserialized {} bullets.".format(len(bulletDictionary)))

	with open("bin/NameDictionary.pkl", "rb") as f:
		nameDictionary = pickle.load(f)

	with open("bin/TileDictionary.pkl", "rb") as f:
		tileDictionary = pickle.load(f)       
		print("[Initializer]: Deserialized {} tiles.".format(len(tileDictionary)))

	with open("bin/AoeDictionary.pkl", "rb") as f:
		aoeDictionary = pickle.load(f)
		print("[Initializer]: Deserialized {} AOE's from {} enemies.".format(sum({y: len(aoeDictionary[y]) for y in aoeDictionary}.values()), len(aoeDictionary)))

	print("[Initializer]: Starting proxy...")
	client = Client(plugins, bulletDictionary, nameDictionary, tileDictionary, aoeDictionary)
	proxy = Proxy(plugins, client)

	threading.Thread(target = proxy.Start, daemon = True).start()

	print("[Initializer]: Proxy started!")

	print("[Initializer]: Starting GUI...")
	gui = GUI(plugins, client, proxy)
	print("[Initializer]: GUI started!")

	logger = Logger()
	logFile = logger.openLogFile()
	
	gui.start()


if __name__ == "__main__":
	main()