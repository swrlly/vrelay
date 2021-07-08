# Writing your own Plugins

Here's everything you need to know about adding custom plugins to vrelay. We will discuss what a packet is, understanding how to define packet hooks, and how to use vrelay to its fullest potential.

## What is a packet?

A packet is an array of bytes. Developers beforehand have agreed on what certain bytes mean. In RotMG, the first five bytes of a packet tell us how long the actual packet will be and the type of packet this will be. This first five bytes is called the **header**. The rest of the data represent various information about the packet, such as user location, shoot angle, etc. This part of the packet is called the **body**. Packets are sent whenever the client takes some action (such as moving, putting stuff into vault, shooting, hitting an enemy, etc.) or when the server informs us of some new information (such as your friend loading into realm, what's on the market, when an enemy shoots, etc.).

In RotMG, the body of the packet has been encrypted, meaning the actual bytes have been scrambled. We will not go in depth on this here; just know this has been abstracted away from you if you wish to write plugins.

Now we know what a packet is, when it's sent, we can now move on to understanding how to modify it to our own wishes.

## What is a plugin?

In vrelay, a plugin is a python file containing a class. This class will contain some important class variables and some important handlers.

Let's look at a simple plugin `Godmode.py` to get a quick understanding on what a plugin looks like:

```Python
from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from client import Client

class Godmode(PluginInterface):

	hooks = {PacketTypes.PlayerHit, PacketTypes.GroundDamage}
	load = True
	defaultState = False

	def onPlayerHit(self, client: Client, packet: PlayerHit, send: bool) -> (PlayerHit, bool):
		return (packet, False)

	def onGroundDamage(self, client: Client, packet: GroundDamage, send: bool) -> (GroundDamage, bool):
		return (packet, False)

	def getAuthor(self):
		return "swrlly - https://github.com/swrlly"
```

From here, we will use this plugin as a running example.

## Packet hooking + declaring packet hooks

The defining feature behind any plugin is being able to "hook" packets. Hooking a packet is not dissimilar to inserting function hooks in assembly language: main idea is to be able to look inside the packet passing by, and possibly modifying it / updating information we're keeping locally. 

We can break `Godmode.py` down into two main ideas:
1.  You ***must*** declare and initialize class variables `hooks`, `load`, and `defaultState`. 
   - `hooks` is a set data structure that tells vrelay which packets you intend to hook. You can find all packet types [in valorlib](https://github.com/swrlly/valorlib/blob/main/Packets/PacketTypes.py), the networking library for vrelay. 
   - `load` is a boolean that tells vrelay whether you wish to load this plugin or not. 
      - If `True`, this plugin will be available for you throughout the duration of vrelay. 
      - If `False`, then this plugin will be disabled and not loaded during initialization. This is useful if you wish to disable some plugins.
   -  `defaultState` is a boolean that tells vrelay after loading the plugin, will the plugin be on or off? 
      - If `True`, then the plugin will already be on when you start vrelay. This is useful if you wish to write a plugin that is always on in the background, but doesn't need to appear in the GUI.
      - If `False`, then the plugin will be off when you start vrelay.
2. For each packet type you put into `hooks`, you need to write a handler to take care of that exact packet type as it passes by. This handler is what enables vrelay to hook packets.
   - The naming convention of this handler is `on` + [the capitalization found in `PacketTypes.py.`](https://github.com/swrlly/valorlib/blob/main/Packets/PacketTypes.py)
      - Example: from the above example, we wish to hook the packet types `PlayerHit` and `GroundDamage`. Thus, the two handlers we wrote to hook these packets were named `onPlayerHit` and `onGroundDamage`, respectively.
   - Function parameters: there are four function parameters: `self, client, packet,` and `send`.
      - `self`: self-explanatory as this handler is a class function.
      - `client`: an instance of the `Client` class, which contains important variables about your character (such as current HP, current location, etc.) and functions to send packets.
      - `packet`: this is an instance of the type of packet you hooked. In the above example, we can see for `onGroundDamage`, packet is an instance of the packet type `GroundDamage`. You can find all the implemented packet types [in the `incoming/outgoing` folders in valorlib](https://github.com/swrlly/valorlib/tree/main/Packets).
      - `send`: a boolean that informs whether you wish to send this packet to it's intended destination.
         - It is recommended never to set `send = True` as this can interfere with the behavior of other plugins if other plugins set `send = False` already.
   - Return type: a tuple consisting of the two parameters you passed in: `packet` and `send`.
      - Example: From above, you can see in `onGroundDamage`, we return the original packet we passed in, but set send to `False`. 

If the above explanation and example does not suffice, read the [type hints](https://www.python.org/dev/peps/pep-0484/) in other plugins to get a better feel for how other packet types were hooked and how the handlers were declared.

## What's next?

Now that we have handlers, we can block packets from being sent to their destination. But we can also modify packets as they pass by. We can also decrypt packets to get an idea of what's going on in real time instead of waiting for the server to update us every 0.2 seconds.
- [Take a look at `Plugins/NoDebuff.py`](https://github.com/swrlly/vrelay/blob/main/Plugins/NoDebuff.py) to see an in-depth example on how the `NewTick` packet was modified to remove any negative status effects we might have.
- [Take a look at `Plugins/AutoNexus.py`](https://github.com/swrlly/vrelay/blob/main/Plugins/AutoNexus.py) to see an in-depth example on how I hooked multiple packets, calculating an internal HP value (before server updates us), and predicted AoE's before they landed.