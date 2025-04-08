import json
import os
import shutil

INDEX_PATH = "track_index.json"

def load_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_index(index):
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4, ensure_ascii=False)

def processar_faixa(track_id, track_title, playlist_name, index, base_path):
    """
    Decide se a música deve ser baixada, copiada ou ignorada, com base no índice atual e nas localizações reais.
    """
    new_path = os.path.join(playlist_name, track_title + ".mp3")
    full_new_path = os.path.join(base_path, new_path)

    # Se a track ainda não existe no index
    if track_id not in index:
        print(f"[⬇️] Nova faixa: {track_title} → {playlist_name}")
        index[track_id] = {
            "name": track_title,
            "playlists": [playlist_name],
            "current_locations": []
        }
    else:
        # Adiciona a playlist mesmo que o arquivo não esteja disponível
        if playlist_name not in index[track_id]["playlists"]:
            index[track_id]["playlists"].append(playlist_name)

    localizacoes = index[track_id].get("current_locations", [])

    if new_path in localizacoes:
        print(f"[✔] Já sincronizado: {track_title} em {playlist_name}")
        return

    # Se já existe fisicamente mas não está no index
    if os.path.exists(full_new_path):
        print(f"[🧩] Arquivo já estava lá, adicionando ao index: {new_path}")
        localizacoes.append(new_path)
        return

    # Tenta copiar de alguma pasta existente
    origem = None
    for loc in localizacoes:
        origem_path = os.path.join(base_path, loc)
        if os.path.exists(origem_path):
            origem = origem_path
            break

    if origem:
        os.makedirs(os.path.dirname(full_new_path), exist_ok=True)
        shutil.copy2(origem, full_new_path)
        print(f"[📁] Copiado {track_title} para {playlist_name}")
        localizacoes.append(new_path)
    else:
        print(f"[❗] Arquivo não encontrado para copiar: {track_title}")

def remover_localizacao(track_id, path_relativa, index):
    if track_id in index and "current_locations" in index[track_id]:
        if path_relativa in index[track_id]["current_locations"]:
            index[track_id]["current_locations"].remove(path_relativa)
