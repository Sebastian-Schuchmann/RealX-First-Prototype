import Spotify as Spotify

# INIT (CALL THIS FIRST ALWAYS)
spotifyUser = Spotify.initialize()
Spotify.playPlaylistByName(spotifyUser, Spotify.DEEPWORK)

# PAUSE PLAYBACK
#Spotify.pausePlayback(spotifyUser)

# CONTROL VOLUME 0 to 100
spotifyUser.volume(30)

