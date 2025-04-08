import os
from yt_dlp import YoutubeDL

def baixar_musica(track_title, pasta_destino):
    """
    Faz o download de uma música a partir do YouTube usando yt-dlp.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    destino_path = os.path.join(pasta_destino, f"{track_title}.mp3")

    if os.path.exists(destino_path):
        print(f"[✔] Já baixado: {track_title}")
        return destino_path

    print(f"[🎶] Baixando: {track_title}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': destino_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([track_title])
        return destino_path
    except Exception as e:
        print(f"[❌] Erro ao baixar {track_title}: {e}")
        return None


def baixar_musicas_faltantes(index, base_path):
    for track_id, dados in index.items():
        if not dados["current_locations"]:
            primeira_playlist = dados["playlists"][0]
            pasta_destino = os.path.join(base_path, primeira_playlist)
            destino = baixar_musica(dados["name"], pasta_destino)

            if destino:
                # Atualiza o caminho relativo
                rel_path = os.path.relpath(destino, base_path)
                dados["current_locations"].append(rel_path)