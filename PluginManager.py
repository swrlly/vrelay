class PluginManager:


	def __init__(self):
		# key is plugin class, value is true if on else false
		self.plugins = {}
		# key is packet type, value is set of plugin classes (key for self.plugins)
		self.hooks = {}
		# tell the manager which plugins will always be on, this is string of class name
		self.alwaysOn = ["DamageBoost", "TeleportTools"]

	"""
	initialize all plugins.
	creates a dictionary with key
	returns true if success, false o.w. 
	"""
	def initializePlugins(self) -> bool:

		import os
		for plugin in os.listdir("Plugins"):
			if plugin[-3:] == ".py":
				t = plugin.replace(".py", "")
				exec("from Plugins.{} import *".format(t))
				try:
					# by default, the plugin is not active.
					if eval(t).load == True:

						if eval(t).defaultState == True:
							self.plugins.update({eval(t + "()") : True})
						else:
							self.plugins.update({eval(t + "()") : False})
				except Exception as e:
					print("There was an error when loading plugins. Make sure you follow the naming convention when writing your own plugins.")
					print("Error:", e)
					return False

		print("[Initializer]: Successfully loaded {} plugins.".format(len(self.plugins)))
		return True

		
	# returns relevant class you searched for
	def findClass(self, text: str):
		for plugin in self.plugins:
			if type(plugin).__name__ == text:
				return plugin

	"""
	Creates a dictionary with key = PacketType, value = key of plugins
	allows us to just call specific plugins on specific packets
	"""
	def initializeHookDictionary(self):
		for plugin in self.plugins:
			for hook in plugin.hooks:
				# add new packettype hook
				if hook not in self.hooks:
					self.hooks.update({hook : {plugin}})
				# already exists
				else:
					self.hooks[hook].add(plugin)

	def initialize(self):
		if not self.initializePlugins():
			return False
		self.initializeHookDictionary()
		return True