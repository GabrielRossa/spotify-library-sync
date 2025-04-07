def get_tracks_from_playlist(sp, playlist_id):
    tracks = {}
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            if not track:
                continue

            track_id = track['id']
            name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            full_title = f"{', '.join(artists)} - {name}"

            tracks[track_id] = full_title

        if results['next']:
            results = sp.next(results)
        else:
            break

    return tracks
