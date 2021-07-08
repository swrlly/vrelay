# vrelay

A man-in-the-middle proxy server for the Realm of the Mad God (RotMG) private server Valor. Features packet editing/hooking, a framework to write custom plugins, and many QoL plugins such as predictive autonexus.

For any questions, join the discord: https://discord.gg/nfmQYtUaGS

**Updated for Valor version 3.2.4.**

<p align="center">
  <img src="images/vrelay.png" />
</p>


## How to use

1. Install Python 64-bit. You can find installations of Python [here](https://www.python.org/downloads/). Install the 64-bit version or the GUI will not work.
2. Navigate to the right side of this page and look for `Releases`. Click on the latest release and download from `vrelay-v3.2.4.zip`. 
   - You can also clone this repository.
3. There are two folders, `challenge` and `normal`. The `normal` folder contains the `Valor.swf` file for the normal server. Replace the original `Valor.swf` downloaded from Valor's website with the `Valor.swf` in this folder. In a similar fashion, the `challenge` folder contains a `Valor.swf` file for the challenge league.  Replace this as well (with the respective challenge league `swf`) if you wish to play the challenge league.
     - This `.swf` file has been modded so you can connect to the proxy server. If you only see `Valor`, that means you have your file extensions off.
4. Open the command line (type `Win ⊞ + r` and type in `cmd`, press enter. the command line will now be open), `cd` into the folder containing the code.
    - This will involve typing `cd C:\path\to\folder` then pressing enter.
    - If you downloaded the hack in another drive, such as `Z:` or `D:`, then you need to type the drive name (`Z:` or `D:`, respectively) in order to tell command prompt you wish to be in that drive.
5. Once you're in the folder in the command prompt, type `python proxy.py` in the command line to start the proxy. If you have previously installed Python, also try `py proxy.py` or `python3 proxy.py` if this does not work.
6. Connect to the proxy server in the server list and you're good to go.

## Features

Watch this video for a demonstration of some vrelay features: https://www.youtube.com/watch?v=V9N08Xuop4g

**Toggles**

Each feature has a toggle key as shown in the image above.

1. **Predictive Autonexus**: If you take damage that will put you under a certain threshold, you automatically join the nexus.
    - Accounts for most AoE's except for enemies with 2+ same color throws.
2. **Godmode**: Immune to all bullet and ground damage. Does not block AoE damage.
3. **No projectile**: Hides all projectiles from appearing; essentially another godmode (but very obvious to others as you do not know where to dodge).
    - Does not hide AoE damage (you will still take damage from AoE). 
4. **Speedy**: Apply speedy to yourself!
5. **Swiftness**: Apply swiftness (stronger form of Speedy) to yourself! Stacks with Speedy.
6. **Remove client-side debuffs**: This will remove client-side debuffs one tick after they are applied. These will not remove server-sided debuffs like bleeding, quiet, etc.
7. **Challenge/Normal mode**: This button (in the bottom right corner) will toggle between the proxy connecting to the challenge server or normal server.

**Player commands**

- `/dep`: deposit all potions into your potion storage. Can use this in any map.
- `/an #`: set autonexus % between 0 and 99. Enter only integers.
    - `/an help` in game to see the syntax.
- `/safe`: disable all commands shown above and autonexus messages.

## Writing your own plugins
Will document this section later. For now:

- See `Plugins/Godmode.py` for an explanation on what functions to implement.
- See `Plugins/Speedy.py` to see an in-depth example on how the `NewTick` packet was modified to apply speedy.
- See `Plugins/AutoNexus.py` to see an extremely in-depth example on how to hook multiple packets and keep an internal HP state.

## Notes
I will not be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software. You agree to use vrelay at your own risk and for educational purposes only.

## Credits
- [JPEXS](https://www.free-decompiler.com/flash/download/) for reverse engineering and modifying the client. Huge help for being able to peek into the contents of `swf` files.
- This project is inspired by [KRelay](https://github.com/TheKronks/KRelay), an open source proxy for production RotMG.

#### TODO:
- If Godmode and either Speedy/Swiftness are active, all negative status effects are cancelled (due to PlayerHit being blocked).
- Block all status effects (by checking bullet type)