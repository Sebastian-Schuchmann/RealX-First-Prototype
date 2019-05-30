import sys
import rtmidi
import threading
from importlib.machinery import SourceFileLoader

Spotify = SourceFileLoader("Spotify.py", "Spotify/Spotify.py").load_module()
LightController = SourceFileLoader("LightController.py", "Lights/LightController.py").load_module()
Spotify.initialize()

LightController.setLights(254,0)

midiin = rtmidi.RtMidiIn()
spotifyUser = Spotify.initialize()
pausentimer = 0

# COLOR TEMPERATURES
COLD = 0
NORMAL = 1
WARM = 2


def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "G#0":
        print('Pause')
        Spotify.playPlaylistByName(spotifyUser, Spotify.BREAK)
        LightController.setLights(254,2)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "C0":
        print('Deep Work')
        Spotify.playPlaylistByName(spotifyUser, Spotify.DEEPWORK)
        LightController.setLights(254,0)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "E-1":
        print('Casual Work')
        Spotify.playPlaylistByName(spotifyUser, Spotify.CASUALWORK)
        LightController.setLights(127,0)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "G#-2":
        print('Freizeit')
        Spotify.playPlaylistByName(spotifyUser, Spotify.FREIZEIT)
        LightController.setLights(254,1)
    elif midi.getControllerNumber() == 7:
        spotifyUser.volume(midi.getControllerValue())
    elif midi.getControllerNumber() == 48:
        pausentimer = midi.getControllerValue()
        print('Timer auf:', pausentimer)
        if pausentimer <= 5:
            print('Micropause')
        elif pausentimer <= 25:
            print('Ritualpause')
        elif pausentimer > 25:
            print('Mittagspause')
    elif midi.isNoteOff():
        print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())

ports = range(midiin.getPortCount())
if ports:
    for i in ports:
        print(midiin.getPortName(i))
    print("Starting RealX") 
    midiin.openPort(0)
    while True:
        m = midiin.getMessage(250) # some timeout in ms
        if m:
            print_message(m)
else:
    print('NO MIDI INPUT PORTS!')


     