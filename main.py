from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

'''
Spotify Time Machine procedural program.
'''

SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
REDIRECT_URI = "https://www.spotify.com/us/"

travel_date = input("What year would you like to travel to? Input as YYYY-MM-DD: ")
travel_year = travel_date.split("-")[0]


response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{travel_date}/")
billboard_text = response.text

soup = BeautifulSoup(billboard_text, "html.parser")

songs = soup.find_all(name="h3", class_="a-no-trucate")
artists = soup.find_all(name="span", class_="u-letter-spacing-0021")

song_titles = [song.getText().replace("\n\n\t\n\t\n\t\t\n\t\t\t\t\t", "").replace("\t\t\n\t\n", "") for song in songs]
artists_list = [artist.getText().replace("\n\t\n\t", "").replace("\n", "") for artist in artists]

print(artists_list)
print(song_titles)

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt")
)

user_id = sp.current_user()['id']

songs_uri = []
for _ in range(len(song_titles)):
    result = sp.search(q=f"track:{song_titles[_]} artist:{artists_list[_]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song_titles[_]} doesn't exist in Spotify. Skipped")

print(songs_uri)

playlist = sp.user_playlist_create(user=user_id, name=f"{travel_date} Billboard 100", public=False, collaborative=False,
                        description="Billboards top 100 songs from that year.")
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=songs_uri)