import requests
import base64
# To be filled by the user.
client_id = ''
client_secret = ''
playlist_id = ''
# DO NOT TOUCH THIS!!!!!
def get_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to get token: " + response.json()['error_description'])

def get_playlist_tracks(token, playlist_id):
    base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    tracks = []
    params = {"limit": 100}  # Fetch up to 100 tracks at a time (pagination required for larger playlists)
    
    while True:
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()

        if 'items' not in data:
            break

        for item in data['items']:
            if item['track'] is not None:
                track_url = item['track']['external_urls']['spotify']
                tracks.append(track_url)

        if data['next']:
            params['offset'] = len(tracks)
        else:
            break

    return tracks


def save_to_file(track_urls, filename='spotify_song_links.txt'):
    with open(filename, 'w') as f:
        for url in track_urls:
            f.write(url + '\n')
    print(f"Saved {len(track_urls)} track links to {filename}.")

if __name__ == '__main__':
    token = get_token(client_id, client_secret)
    tracks = get_playlist_tracks(token, playlist_id)
    save_to_file(tracks)
