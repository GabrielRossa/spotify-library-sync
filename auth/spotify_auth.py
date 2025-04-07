from spotipy.oauth2 import SpotifyOAuth
import spotipy
import json

def get_spotify_client():
    with open("config.json") as f:
        config = json.load(f)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        redirect_uri=config["redirect_uri"],
        scope="playlist-read-private"
    ))

    return sp
