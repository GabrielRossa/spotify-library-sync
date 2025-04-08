from auth.spotify_auth import get_spotify_client
from downloader.yt_downloader import baixar_musicas_faltantes
from spotify.playlists import listar_playlists
from spotify.tracks import get_tracks_from_playlist
from sync.folder_manager import criar_pasta_para_playlist
from sync.sync_engine import load_index, save_index, processar_faixa

import os

BASE_PATH = os.path.join(os.getcwd(), "SET_DJ")

def main():
    sp = get_spotify_client()
    playlists = listar_playlists(sp)
    index = load_index()

    # Mapeia cada track_id para as playlists onde ela aparece no Spotify
    playlists_atuais_por_track = {}

    for playlist in playlists:
        nome = playlist['name']
        playlist_id = playlist['id']
        categoria = playlist.get('categoria')  # Não será mais usado se você removeu a lógica de categoria

        print(f"\n🎵 Playlist: {nome} ({playlist['tracks']} músicas)")

        # Cria a pasta da playlist
        criar_pasta_para_playlist(BASE_PATH, nome, categoria)

        # Coleta as faixas da playlist
        tracks = get_tracks_from_playlist(sp, playlist_id)

        for track_id, track_title in tracks.items():
            # Registra em quais playlists a música aparece
            if track_id not in playlists_atuais_por_track:
                playlists_atuais_por_track[track_id] = []
            playlists_atuais_por_track[track_id].append(nome)

            # Processa a faixa
            processar_faixa(track_id, track_title, nome, index, BASE_PATH)

    # Atualiza o campo "playlists" de cada track com as playlists reais
    for track_id, playlists_atuais in playlists_atuais_por_track.items():
        if track_id in index:
            index[track_id]["playlists"] = playlists_atuais

    save_index(index)
    # baixar_musicas_faltantes(index, BASE_PATH)
    save_index(index)


if __name__ == "__main__":
    main()
