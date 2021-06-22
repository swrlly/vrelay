# vrelay

A man-in-the-middle proxy server for the Realm of the Mad God (RotMG) private server Valor. 

**Updated for Valor version 3.2.4.**

<p align="center">
  <img src="vrelay v2.png" />
</p>


## How to use

For any questions, join the discord: https://discord.gg/nfmQYtUaGS

1. Install Python 64-bit. You can find installations of Python [here](https://www.python.org/downloads/). Install the 64-bit version or the GUI will not work.
2. A download link to the hack will be provided below. In this step, download the hack and unzip it.
3. There are two folders, `challenge` and `normal`. The `normal` folder contains the `Valor.swf` file for the normal server. Replace the original `Valor.swf` downloaded from Valor's website with the `Valor.swf` in this folder. In a similar fashion, the `challenge` folder contains a `Valor.swf` file for the challenge league.  Replace this as well (with the respective challenge league `swf`) if you wish to play the challenge league.
     - This `.swf` file has been modded so you can connect to the proxy server. If you only see `Valor`, that means you have your file extensions off.
4. Open the command line (type `⊞ + r` and type in `cmd`, press enter. the command line will now be open), `cd` into the folder containing the code.
    - This will involve typing `cd C:\path\to\folder` then pressing enter.
    - If you downloaded the hack in another drive, such as `Z:` or `D:`, then you need to type the drive name (`Z:` or `D:`, respectively) in order to tell command prompt you wish to be in that drive.
5. Once you're in the folder in the command prompt, type `python proxy.py` in the command line to start the proxy. If you have previously installed Python, also try `py proxy.py` or `python3 proxy.py` if this does not work.
6. Connect to the proxy server in the server list and you're good to go.


## Features

Watch this video for a demonstration of some vrelay features: https://www.youtube.com/watch?v=V9N08Xuop4g

**Toggles**

- **Godmode**: Immune to all bullet and ground damage. Does not block AoE damage.
- **No projectile**: Hides all projectiles from appearing; essentially another godmode (but very obvious to others as you do not know where to dodge).
    - Does not hide AoE damage (you will still take damage from AoE). 
- **Speedy**: Apply speedy to yourself!
- **Swiftness**: Apply swiftness (stronger form of Speedy) to yourself! Stacks with Speedy.
- **Remove client-side debuffs**: This will remove client-side debuffs one tick after they are applied. These will not remove server-sided debuffs like bleeding, quiet, etc.
- **Autonexus**: If you take damage that will put you under a certain threshold, you automatically join the nexus.
    - ***Does NOT account*** for AoE right now. Working on collecting data to add predictive AoE autonexus.
- **Shut down all plugins**: This will turn off all active plugins. Reduces amount of clicking you need to do if you have many plugins active.
- **Challenge/Normal mode**: This button will toggle between the proxy connecting to the challenge server or normal server.

**Player commands**

- `/dep`: deposit one potion of each type into your potion storage. Can use this in any map.
- `/an #`: set autonexus % between 0 and 99. Enter only integers.
    - `/an help` in game to see the syntax.

## Writing your own plugins
Will document this section later. For now:

- See `Plugins/Godmode.py` for an explanation on what functions to implement.
- See `Plugins/Speedy.py` to see an in-depth example on how the `NewTick` packet was modified to apply speedy.
- See `Plugins/AutoNexus.py` to see an extremely in-depth example on how to hook multiple packets and keep an internal HP state.




## Notes
I am not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk. Educational purposes only!

## Credits
- [JPEXS](https://www.free-decompiler.com/flash/download/) for reverse engineering and modifying the client. Huge help for being able to peek into the contents of `swf` files.
- This project is inspired by [KRelay](https://github.com/TheKronks/KRelay), an open source proxy for production RotMG.

#### TODO:
- If Godmode and either Speedy/Swiftness are active, all negative status effects are cancelled. (due to PlayerHit being blocked).
- Block all status effects (by checking bullet type)