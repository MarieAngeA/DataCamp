import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import pandas as pd

# Charger les données
data = pd.read_csv('datacampv2.csv')
artists = data['Artist'].unique().tolist()
genres = data['Genre'].unique().tolist()
songs = data['Title'].unique().tolist()

st.header("Welcome to our Music Recommendation", divider='rainbow')

CLIENT_ID = "d015419636d6430ab1534d3e0e122e8a"
CLIENT_SECRET = "60523d7d723940b3b5e1755ca10fef08"
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

if 'recommended_by_artist' not in st.session_state:
    st.session_state.recommended_by_artist = None

if 'recommended_by_title' not in st.session_state:
    st.session_state.recommended_by_title = None

def recommendation_artist_and_genre(data, artists, genres):
    st.subheader("Recommend based on artist and genre")

    selected_artists = st.multiselect('Please choose an artist:', artists)
    if len(selected_artists) > 3:
        st.warning("You can choose up to 3 artists.")

    selected_genre = st.selectbox('Please select the type of music you want:', genres)

    if st.button('Recommendation'):
        recommended_songs = data[(data['Artist'].isin(selected_artists)) & (data['Genre'] == selected_genre)]
        st.session_state.recommended_by_artist = recommended_songs

    if st.session_state.recommended_by_artist is not None:
        recommended_music_names = st.session_state.recommended_by_artist['Title'].tolist()
        recommended_music_posters = [get_song_album_cover_url(song, artist) for song, artist in zip(st.session_state.recommended_by_artist['Title'], st.session_state.recommended_by_artist['Artist'])]

        num_songs = len(recommended_music_names)
        
        if num_songs > 0:
            cols = st.columns(num_songs)
            for idx in range(num_songs):
                song_name = recommended_music_names[idx]
                artist_name = st.session_state.recommended_by_artist.iloc[idx]['Artist']
                with cols[idx]:
                    st.write(f"{song_name} par {artist_name}")
                    st.image(recommended_music_posters[idx], width=150)
        else:
            st.write("Aucune recommandation trouvée pour les artistes et le genre sélectionnés.")



def recommendation_song_title(data, songs):
    st.subheader("Recommend based on song title")

    selected_song = st.selectbox("Select a song title:", songs)

    if st.button('Recommendation Title'):
        song_genre = data[data['Title'] == selected_song].iloc[0]['Genre']
        recommendations = data[data['Genre'] == song_genre].sample(5)
        st.session_state.recommended_by_title = recommendations

    if st.session_state.recommended_by_title is not None:
        recommendations = st.session_state.recommended_by_title
        cols = st.columns(5)
        for idx, (index, row) in enumerate(recommendations.iterrows()):
            song_name = row['Title']
            artist_name = row['Artist']
            cover_url = get_song_album_cover_url(song_name, artist_name)

            with cols[idx]:
                st.write(f"{song_name} par {artist_name}")
                st.image(cover_url, width=150)

recommendation_artist_and_genre(data, artists, genres)
recommendation_song_title(data, songs)

st.write("Thanks for using our application!")
st.write('_Hope you :blue[enjoyed] !_  :sunglasses:')
