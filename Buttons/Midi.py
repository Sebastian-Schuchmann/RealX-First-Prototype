import sys
import rtmidi
import threading
from importlib.machinery import SourceFileLoader
from subprocess import check_output

Spotify = SourceFileLoader("Spotify.py", "Spotify/Spotify.py").load_module()
Spotify.initialize()

midiin = rtmidi.RtMidiIn()
spotifyUser = Spotify.initialize()
pausentimer = 0

def get_result(cmd, args):
  out_put = check_output("%s %s" % (cmd, args), shell=True)
  return out_put

dir = "Directory: "
files = get_result("ls", dir)
for file in files.split(' '):
  for f in file.split('\n'):
    results = get_result("dunkel.scpt", f)
    
    print(results)

def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "G#0":
        print('Pause')
        Spotify.playPlaylistByName(spotifyUser, Spotify.BREAK)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "C0":
        print('Deep Work')
        Spotify.playPlaylistByName(spotifyUser, Spotify.DEEPWORK)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "E-1":
        print('Casual Work')
        Spotify.playPlaylistByName(spotifyUser, Spotify.CASUALWORK)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "G#-2":
        print('Freizeit')
        Spotify.playPlaylistByName(spotifyUser, Spotify.FREIZEIT)
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


     