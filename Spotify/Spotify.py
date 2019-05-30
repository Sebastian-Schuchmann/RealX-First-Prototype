import sys
import spotipy
import json
import spotipy.util as util

#CHANGE THIS TO YOUR ACCOUNT VALUES
CLIENT_ID = "8bd76f87395b4a8dbbdfa4c9ad9ab703"
CLIENT_SECRET = "1191c291afdc4831a6ac486e195a21a7"
USERNAME = "Fansep"


#DEFINE PLAYLISTS MANUALLY
DEEPWORK = "Deep Work"
CASUALWORK = "Casual Work"
BREAK = "Break"
FREIZEIT = "Freizeit"



def playPlaylistByName(spotifyUser, name):
    playlists = spotifyUser.current_user_playlists(limit=50)
    foundPlaylist = False
    
    for i in playlists["items"]:
        #print(json.dumps(i, indent=4, sort_keys=True))
        if i["name"] == name:
            uri = i["uri"]
            foundPlaylist = True
            break

    if foundPlaylist:
        spotifyUser.start_playback(device_id = None, context_uri=uri)
    else:
        print("Playlist not found")

def pausePlayback(spotifyUser):
    spotifyUser.pause_playback()

def initialize():
    # Define what the application is allowed to do
    scope = 'streaming user-read-currently-playing user-follow-read user-modify-playback-state app-remote-control user-read-private user-read-playback-state user-library-read playlist-read-private user-library-modify user-library-read'
    username = USERNAME

    # Request Token from Spotify to get access to account
    token = util.prompt_for_user_token(username,scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri='http://localhost/')

    # Check if token is valid
    if token:
        sp = spotipy.Spotify(auth=token)
        return sp
       
    else:
        print ("Can't get token for", username)
        return None







