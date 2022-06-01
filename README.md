# Platform3
A NYC subway countdown clock within the comforts of your own home.

![Gif of home made subway countdown clock with cool reflection over wooden table](https://user-images.githubusercontent.com/5365169/171101291-5e7b06ce-0cba-47dd-8b86-aed2dba16a6f.gif)

## Parts
Part | My cost | Link (and your cost)
-|-|-
32x64 LED matrix + cables | $20 (matrix from Taobao, cables from Tinkersphere) | [Adafruit](https://www.adafruit.com/product/2276) (includes cables), [16 pin cable only](https://tinkersphere.com/cables-wires/1973-16-pin-2x8-ribbon-cable.html), [4 pin power only](https://tinkersphere.com/led-matrix-panels/1229-0-15-pitch-4-pin-power-cable-w-spade-connectors.html)
Raspberry Pi | $50 (3B+) | Any good Pi, Zero 2 W is good but sold out
Adafruit RGB matrix bonnet | $15 | [Adafruit](https://www.adafruit.com/product/3211) or on Digikey
Power supply and wall plug | $25 5V 10A | [Tinkersphere](https://tinkersphere.com/power/830-5v-10a-dc-power-adapter.html) (doesn't include wall plug)
Shipping | ~$15 for local parts | -

## Assembly
1. **Tools: Keyboard, Mouse, and Monitor** Setup raspberry pi with latest OS and python 3.7+ (already pre-installed)
2. **Tools: Soldering Iron (optional)** Assemble the components according to the [Adafruit](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) guide. Soldering optional under step 6.
3. Continue following the Adafruit software setup until complete.

## Setup
1. Clone/download repository. Enter that directory using `cd <the path of the repository you just cloned>`.
2. Obtain API token by [signing up on MTA](https://api.mta.info/#/signup) and generating a token for GTFS-rt
3. Run `make` to install dependencies and generate `config.py`
4. Edit `config.py` to paste in the API token, and set up the `stops` array as follows: `Stop("<train>", "<stop>", <distance in minutes from station>)`. `<train>` is A, L, 7X, FS, etc. as listed in [VALID_STOP_IDS](platform3/constants.py), `<stop>` is the stop ID _with direction_ obtained from [this list](https://github.com/Andrew-Dickinson/nyct-gtfs/blob/master/nyct_gtfs/gtfs_static/stops.txt), and `<distance in minutes from station>` is used to filter out trains that arrive too soon for you to be concerned.
5. Run with the following commands: `chmod +x platform3/platform3.py` (enables execution), `sudo su` (elevates privilege to run low level hardware stuff), `platform3/platform3.py` (runs the program).

## Help
This is a work in progress. Make an issue or a pull request and we'll address it when we can!
