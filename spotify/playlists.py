def passa_filtro(nome_playlist):
    nome_lower = nome_playlist.lower().strip()

    # Finais
    finais_validos = ['house', 'techno', 'bass', 'trance']
    for f in finais_validos:
        if nome_lower.endswith(f):
            return True, f.capitalize()  # Ex: 'House'

    # Inícios
    inicios_validos = ['set', 'old']
    for i in inicios_validos:
        if nome_lower.startswith(i):
            return True, i.upper()  # Ex: 'SET'

    # Nomes exatos
    nomes_especificos = [
        'data lake',
        'duos'
    ]
    if nome_lower in [n.lower() for n in nomes_especificos]:
        return True, 'Específicas'

    return False, None



def listar_playlists(sp):
    print("=== LISTANDO PLAYLISTS FILTRADAS ===\n")
    playlists = []

    me = sp.current_user()
    meu_id = me['id']

    results = sp.current_user_playlists()

    while results:
        for playlist in results['items']:
            name = playlist['name']
            playlist_id = playlist['id']
            track_count = playlist['tracks']['total']
            owner_id = playlist['owner']['id']
            owner_name = playlist['owner']['display_name'] or playlist['owner']['id']

            # Filtro: só playlists criadas por você
            if owner_id != meu_id:
                continue

            # Filtro: nome válido e categoria
            passou, categoria = passa_filtro(name)
            if not passou:
                continue

            print(f"[✓] {name} | ID: {playlist_id} | {track_count} músicas | Categoria: {categoria} | Criada por: {owner_name}")

            playlists.append({
                'name': name,
                'id': playlist_id,
                'tracks': track_count,
                'owner': owner_name,
                'categoria': categoria
            })

        if results['next']:
            results = sp.next(results)
        else:
            break

    return playlists
