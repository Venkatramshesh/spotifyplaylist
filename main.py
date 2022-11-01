import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import cred
import os

date = input("Which year do you want to travel to?Type the date in this fromat YYYY-MM-DD ")
year = (date[0:4])
URL = "https://www.billboard.com/charts/hot-100/"+f"{date}/"

response = requests.get(URL)
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage,"html.parser")
#print(soup)

song_list = (soup.find_all(name="h3", id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"))

#print(song_list)
song_title = []
song_number = []

song_list1=soup.find(name="h3", id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")

for songs in song_list1:
     song_title.append(songs.text)

#song_list = soup.find_all(name="h3", id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

for songs in song_list:
     song_title.append(songs.text)


SPOTIPY_CLIENT_ID= os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret= SPOTIPY_CLIENT_SECRET, redirect_uri="http://example.com",scope='playlist-modify-public',open_browser=False))
username=sp.current_user()["id"]

playlist = sp.user_playlist_create(username, name=f"{date}" + " billboard100", public=True, collaborative=False, description="Top100")
#print(playlist['id'])
song_uri=[]

for songs in song_title:
     #print(songs)
     try:
          result_song = sp.search(q="track:" +f"{songs}"+ "year:" +f"{year}" , type='track')
          song_uri.append(result_song['tracks']['items'][0]['album']['uri'])
     except:
          continue

#print(song_uri)
try:sp.user_playlist_add_tracks(username, playlist['id'], tracks=song_uri, position=None)
except: print("track not found")

