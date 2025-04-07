import json
import os

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


def processar_faixa(track_id, track_title, nova_categoria, index, base_path):
    """
    Decide se a música deve ser baixada, movida ou ignorada, com base no índice atual.
    """
    if track_id not in index:
        print(f"[⬇️] Nova faixa: {track_title} → {nova_categoria}")
        index[track_id] = {
            "name": track_title,
            "categoria": nova_categoria
        }
        return

    categoria_atual = index[track_id]['categoria']

    if categoria_atual != nova_categoria:
        print(f"[🔁] Mover: {track_title} de {categoria_atual} → {nova_categoria}")
        mover_arquivo(track_title, categoria_atual, nova_categoria, base_path)
        index[track_id]['categoria'] = nova_categoria
    else:
        print(f"[✔] Já sincronizado: {track_title} em {nova_categoria}")


def mover_arquivo(track_title, categoria_origem, categoria_destino, base_path):
    from_path = os.path.join(base_path, categoria_origem, track_title + ".mp3")
    to_path = os.path.join(base_path, categoria_destino, track_title + ".mp3")

    if os.path.exists(from_path):
        os.makedirs(os.path.dirname(to_path), exist_ok=True)
        os.rename(from_path, to_path)
        print(f"[📁] Arquivo movido para: {to_path}")
    else:
        print(f"[❗] Arquivo não encontrado para mover: {from_path}")