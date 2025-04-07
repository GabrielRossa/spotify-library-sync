# sync/folder_manager.py

import os

def criar_pasta_para_playlist(base_path, nome_playlist, categoria):
    """
    Cria a pasta local corretamente de acordo com a categoria:
    - 'Específicas' → direto na raiz
    - 'SET' → vira subpasta 'Funk'
    - demais → categoria como subpasta
    """
    if categoria == 'Específicas':
        caminho = os.path.join(base_path, nome_playlist)
    elif categoria == 'SET':
        caminho = os.path.join(base_path, 'Funk', nome_playlist)
    else:
        caminho = os.path.join(base_path, categoria, nome_playlist)

    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"[📁] Criado: {caminho}")
    else:
        print(f"[✔] Já existe: {caminho}")

    return caminho
