# vrelay

A man-in-the-middle proxy server for the Realm of the Mad God (RotMG) private server Valor. Features packet editing/hooking, a framework to write custom plugins, QoL plugins such as predictive autonexus, and data science-based scripts to autoupdate `vrelay`. Also contains patched exploits that can be generalized to any multiplayer game.


<p align="center">
  <img src="images/vrelay.png" />
</p>

# Table of Contents
- [How to update vrelay?](https://github.com/swrlly/vrelay#how-to-update-vrelay)
- [How to use vrelay?](https://github.com/swrlly/vrelay#how-to-use-vrelay)
- [Features](https://github.com/swrlly/vrelay#features)
- [Disclaimer](https://github.com/swrlly/vrelay#disclaimer)
- [Credits](https://github.com/swrlly/vrelay#credits)


## How to update vrelay?
[A README in the `updater` folder](https://github.com/swrlly/vrelay/tree/main/updater) explains what and how to update.

## How to use `vrelay`?

1. Install Python [64-bit](https://www.python.org/downloads/).
2. `git clone --recurse-submodules https://github.com/swrlly/vrelay.git`
3. `py -m pip install -r requirements.txt`
4. `py proxy.py` to start the proxy server.
5. Obtain a way to force the Valor client to connect to localhost. The easiest way to achieve this is to follow instructions in [updater](https://github.com/swrlly/vrelay/tree/main/updater).
5. In Valor, connect to the proxy server in the server list and you're good to go.

## How to write my own plugins?
[A README in the `plugins` folder](https://github.com/swrlly/vrelay/tree/main/Plugins) explains the necessary steps for writing plugins.

## Features

Watch this video for a demonstration of some vrelay features: https://www.youtube.com/watch?v=V9N08Xuop4g

**Toggles**

Each feature has a toggle key as shown in the image above. Keys will only be registered if your focused window is the game.

- `F1` - **Predictive Autonexus**: If you take damage that will put you under a certain threshold, you automatically join the nexus.
    - Accounts for most AoE's except for enemies with 2+ same color throws.
- `F2` - **Godmode**: Immune to all bullet and ground damage. Does not block AoE damage.
- `F3` - **No projectile**: Hides all projectiles from appearing; essentially another godmode (but very obvious to others as you do not know where to dodge).
    - Does not hide AoE damage (you will still take damage from AoE). 
- `F4` - **Speedy**: Apply speedy to yourself!
- `F5` - **Swiftness**: Apply swiftness (stronger form of Speedy) to yourself! Stacks with Speedy.
- `F6` - **Remove client-side debuffs**: This will remove client-side debuffs one tick after they are applied. These will not remove server-sided debuffs like bleeding, quiet, etc.
- `ESC`: Shutdown all plugins.

**Player commands**

- `/dep`: deposit all potions into your potion storage. Can use this in any map.
- `/an #`: set autonexus % between 0 and 99. Enter only integers.
    - `/an help` in game to see the syntax.
- `/safe`: disable all commands shown above and autonexus messages.


## Disclaimer

Digital Millennium Copyright Act (DMCA) USC § 1201 (f) states:

A person who has lawfully obtained the right to use a copy of a computer program may circumvent a technological measure that effectively controls access to a particular portion of that program for the sole purpose of identifying and analyzing those elements of the program that are necessary to achieve interoperability of an independently created computer program with other programs, and that have not previously been readily available to the person engaging in the circumvention, to the extent any such acts of identification and analysis do not constitute infringement under this title.

This repository contains the latest RotMG Valor hacks and hacked client. If you are looking for RotMG Exalt hacks, RotMG Unity hacked client, or RotMG dupes (item duplication method) this is not the place.

## Credits
- [JPEXS](https://github.com/jindrapetrik/jpexs-decompiler/releases) for reverse engineering and modifying the client. 
- This project is inspired by [KRelay](https://github.com/TheKronks/KRelay), an open source proxy for production RotMG.