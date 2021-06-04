# vrelay

A man-in-the-middle proxy server for the Realm of the Mad God (RotMG) private server Valor. 

**Updated for Valor version 3.2.4.**

<p align="center">
  <img src="vrelay v1.png" />
</p>


## How to use

For any questions, join the discord: https://discord.gg/nfmQYtUaGS

1. Install Python 64-bit. You can find installations of Python [here](https://www.python.org/downloads/). Install the 64-bit version or the GUI will not work.
2. A download link to the hack will be provided below. In this step, download the hack and unzip it.
3. Replace your original `Valor.swf` with the `Valor.swf` in the unzipped folder. This `.swf` file has been modded so you can connect to the proxy server. If you only see `Valor`, that means you have your file extensions off.
4. Open the command line (type `⊞ + r` and type in `cmd`, press enter. the command line will now be open), `cd` into the folder containing the code.
    - This will involve typing `cd C:\path\to\folder` then pressing enter.
    - If you downloaded the hack in another drive, such as `Z:` or `D:`, then you need to type the drive name (`Z:` or `D:`, respectively) in order to tell command prompt you wish to be in that drive.
5. Once you're in the folder in the command prompt, type `python proxy.py` in the command line to start the proxy. If you have previously installed Python, also try `py proxy.py` or `python3 proxy.py` if this does not work.
6. Connect to the proxy server in the server list and you're good to go.


## Features

All features have a button in the GUI to turn the hack on or off.

- **Godmode**: Immune to all bullet and ground damage. Does not block AoE damage. See this [YouTube video for a demo.](https://www.youtube.com/watch?v=cNerTN7HwhM)
- **No projectile**: Hides all projectiles from appearing; essentially another godmode (but very obvious to others as you do not know where to dodge).
    - Does not hide AoE damage (you will still take damage from AoE). 
- **Speedy**: Apply speedy to yourself!
- **Swiftness**: Apply swiftness (stronger form of Speedy) to yourself! Stacks with Speedy.
- **Remove client-side debuffs**: This will remove client-side debuffs one tick after they are applied. These will not remove server-sided debuffs like bleeding, quiet, etc.
- **Shut down all plugins**: This will turn off all active plugins. Reduces amount of clicking you need to do if you have many plugins active.
- Ability to write your own plugins! 
- Ability to inject packets.

## Writing your own plugins
Will document this section later. For now:

- See `Plugins/Godmode.py` for an explanation on what functions to implement.
- See `Plugins/Speedy.py` to see an in-depth example on how the `NewTick` packet was modified to apply speedy.


## Notes
- You can use `/dep` to put potions into potion vault anywhere (in dungeons and realms). Currently spams your screen.

## Credits
- [JPEXS](https://www.free-decompiler.com/flash/download/) for reverse engineering and modifying the client.
- This project is inspired by [KRelay](https://github.com/TheKronks/KRelay), an open source proxy for production RotMG.

#### TODO:
- There is a bug where if Godmode and either Speedy/Swiftness are active, all negative status effects are cancelled. While this is great, this is a bug from a software persepective.