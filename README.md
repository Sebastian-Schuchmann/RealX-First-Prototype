# RealX-First-Prototype
By Robin Bittlinger and Sebastian Schuchmann

### Create cues to improve your workflow
This App will defend you against distractions and maximizes your Deep-Work time.

## Install
#### Requirements
1. This Repo currently only works on **MacOS** (Version: >10).

2. You need a MIDI Controller with at least 4 Buttons!
3. Ikea Tradfri Lights (at least 1)
4. Spotify Premium Account

#### Libaries
##### Ikea Tradfri (Pytradfri Libary)
See [this repo](https://github.com/ggravlingen/pytradfri) for help regarding the Lights.

`pip install pytradfri`

`pip install pytradfri[async]`

`brew install autoconf automake libtool`

Goto Install Files directory:

`sh install-coap-client.sh`

##### Midi Controls (RT-MIDI)
`pip install python-rtmidi`

##### Spotify (Spotipy)
`pip install spotipy`

**Pip Install is outdated so you have to replace Client.py that is located in the Install Files folder.**

(*The pip Install can be loacted on different places depending on your OS*)
Path on my Mac: ⁨Macintosh HD⁩ ▸ ⁨Library⁩ ▸ ⁨Frameworks⁩ ▸ ⁨Python.framework⁩ ▸ ⁨Versions⁩ ▸ ⁨3.7⁩ ▸ ⁨lib⁩ ▸ ⁨python3.7⁩ ▸ ⁨site-packages⁩

## Setup
### Lights
Goto `Lights/LightController.py` and change IPAdress and SafetyKey to your Tradfri Gateway IP and SafetyKey. You can find the IP-Adress in your Router Settings and the Safety Key can be found on the back of your Gateway.

### Spotify
Goto `Spotify/Spotify.py` and change these three Values to yours. Checkout the [SpotifyWebAPI](https://developer.spotify.com/documentation/web-api/) for more information:


`CLIENT_ID = ""`

`CLIENT_SECRET = ""`

`USERNAME = ""`

Rememeber: You need a **Spotify Premium** Account for this. 


