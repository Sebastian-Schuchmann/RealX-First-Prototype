import sys
import rtmidi
import threading
from importlib.machinery import SourceFileLoader
import subprocess


Spotify = SourceFileLoader("Spotify.py", "Spotify/Spotify.py").load_module()
LightController = SourceFileLoader("LightController.py", "Lights/LightController.py").load_module()
Spotify.initialize()

LightController.setLights(254,0)


midiin = rtmidi.RtMidiIn()
spotifyUser = Spotify.initialize()

# COLOR TEMPERATURES
COLD = 0
NORMAL = 1
WARM = 2

class MyTimer:
    def __init__(self):
        self.Timer = threading.Timer(70000000, print)
        self.PausenTimer = 1 
    
    def start(self, Duration, function, args):
        self.Timer = threading.Timer(Duration, function, args) 
        self.Timer.start()

    def cancel(self):
        self.Timer.cancel()

    def getPausenTimer(self):
        return self.PausenTimer

    def setPausenTimer(self, newtime):
        self.PausenTimer = newtime

GlobalTimer = MyTimer()



class State:
    def __init__(self, lightTemperature, lightBrightness, Playlist, Duration, DimmOrLight, NextState, Logout):
        self.lightTemperature = lightTemperature
        self.lightBrightness = lightBrightness
        self.Playlist = Playlist
        self.Duration = Duration
        self.DimmOrLight = DimmOrLight
        self.Logout = Logout
        self.IsBreak = False

        
    def switchToState(self, Duration, CurrentActiveState, NextState):
        # A BREAK STATE IS ACTIVE        
        GlobalTimer.cancel()
        
        # SWITCH PLAYLIST AND LIGHT

        Spotify.playPlaylistByName(spotifyUser, self.Playlist)
        if self.DimmOrLight:
              subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "DimmScreenToZero.app"])
        else:
             subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "LightScreenToFull.app"])

        if self.Logout:
            subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "LogOut.app"])

        LightController.setLights(self.lightBrightness, self.lightTemperature)


        # SET TIMER IF BREAK
        print(Duration)
        if Duration > 0:
            self.IsBreak = True
            GlobalTimer.start(Duration*60, NextState.switchToState, [0, self, None])

        return self

# DEFINE POSSIBLE STATES
CasualWorkState = State(0, 178, Spotify.CASUALWORK, 0.0, None, False, False)
DeepWorkState = State(1, 254, Spotify.DEEPWORK, 0.0, None, False, False)
FreizeitState = State(2, 0, Spotify.FREIZEIT, 0.0, None, True, True)
PauseState = State(2, 178, Spotify.BREAK, 0.0, CasualWorkState, True, False)

CurrentState = FreizeitState


def print_message(midi):
    global CurrentState
    CurrentState = FreizeitState
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "G#0":
        print('Pause')
        CurrentState = PauseState.switchToState(GlobalTimer.PausenTimer, CurrentState, CasualWorkState)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "C0":
        print('Deep Work')
        CurrentState = DeepWorkState.switchToState(0, CurrentState, None) 
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "E-1":
        print('Casual Work')
        CurrentState = CasualWorkState.switchToState(0, CurrentState, None)
    elif midi.getMidiNoteName(midi.getNoteNumber()) == "G#-2":
        print('Freizeit')
        CurrentState = FreizeitState.switchToState(0, CurrentState, None)  
    elif midi.getControllerNumber() == 7:
        spotifyUser.volume(midi.getControllerValue())
    elif midi.getControllerNumber() == 48:
        GlobalTimer.PausenTimer = midi.getControllerValue() * 60.0 / 127.0
        GlobalTimer.PausenTimer = int(GlobalTimer.PausenTimer)
        print('Timer auf:', GlobalTimer.PausenTimer)
        if GlobalTimer.PausenTimer <= 5:
            print('Micropause')
        elif GlobalTimer.PausenTimer <= 25:
            print('Ritualpause')
        elif GlobalTimer.PausenTimer > 25:
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


     