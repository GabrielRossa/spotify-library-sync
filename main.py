from auth.spotify_auth import get_spotify_client
from spotify.playlists import listar_playlists
from spotify.tracks import get_tracks_from_playlist
from sync.folder_manager import criar_pasta_para_playlist
from sync.index_tracker import load_index, save_index, processar_faixa

import os

BASE_PATH = os.path.join(os.getcwd(), "SET_DJ")

def main():
    sp = get_spotify_client()
    playlists = listar_playlists(sp)
    index = load_index()

    for playlist in playlists:
        nome = playlist['name']
        playlist_id = playlist['id']
        categoria = playlist['categoria']

        print(f"\n🎵 Playlist: {nome} ({playlist['tracks']} músicas)")

        # Cria a pasta de destino (sem download ainda)
        criar_pasta_para_playlist(BASE_PATH, nome, categoria)

        # Pega as faixas
        tracks = get_tracks_from_playlist(sp, playlist_id)

        for track_id, track_title in tracks.items():
            processar_faixa(track_id, track_title, categoria, index, BASE_PATH)

    save_index(index)

if __name__ == "__main__":
    main()
