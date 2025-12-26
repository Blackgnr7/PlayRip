import requests
import os
import sys
import shutil   
from mutagen.mp4 import MP4,MP4Cover
import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytubefix import YouTube
from pytubefix import Search
from pytubefix.innertube import _default_clients
from pydub import AudioSegment

diretorio_destino = os.path.expanduser("~/Downloads")

class Download():
    def Youtube(url, tipo):
        if(str(tipo).lower() == "mp3"):
            yt = YouTube(url,use_oauth=True, allow_oauth_cache=True)
            thumbnail_peagr = yt.thumbnail_url
            codigo = thumbnail_peagr.split("/")[-2].split("/")[-1]
            thumbnail = "https://i.ytimg.com/vi_webp/" + codigo + "/maxresdefault.webp"
            artist = yt.author
            titulo = yt.title
            titulo_novo1 = titulo.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
            yt.streams.get_audio_only().download(output_path=diretorio_destino)
            res = requests.get(thumbnail, stream=True)
            with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                shutil.copyfileobj(res.raw, out_file)
            caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.m4a"
            with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                img_data = img_file.read()
            sound = AudioSegment.from_file(caminho_arquivo, format="m4a")
            sound.export(f"{diretorio_destino}/{titulo_novo1}.mp3", format="mp3")
            audiofile = eyed3.load(f"{diretorio_destino}/{titulo_novo1}.mp3")
            if not audiofile.tag:
                audiofile.initTag()
            audiofile.tag.artist = artist
            audiofile.tag.images.set(3, img_data, "image/jpeg")
            audiofile.tag.save()
            os.remove(f"{diretorio_destino}/capa.jpg")
            os.remove(f"{caminho_arquivo}")
        if(str(tipo).lower() == "mp4"):
            yt = YouTube(url,use_oauth=True, allow_oauth_cache=True)
            thumbnail_peagr = yt.thumbnail_url
            codigo = thumbnail_peagr.split("/")[-2].split("/")[-1]
            thumbnail = "https://i.ytimg.com/vi_webp/" + codigo + "/maxresdefault.webp"
            artist = yt.author
            titulo = yt.title
            titulo_novo1 = titulo.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
            res = requests.get(thumbnail, stream=True)
            with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                shutil.copyfileobj(res.raw, out_file)
            with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                img_data = img_file.read()
            yt.streams.get_highest_resolution().download(output_path=diretorio_destino)
            caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.mp4"
            video = MP4(caminho_arquivo)
            video["\xa9ART"] = artist
            video["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
            video.save()
            os.remove(f"{diretorio_destino}/capa.jpg")
    def Spotify(url):
        client_id = "82190b6d4e6d4250a7e8d5a16a29443c"
        client_secret = "eb3c7e469f40400b941dc05116cfc55b"
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        track_id = url.split("/")[-1].split("?")[-2]
        track_info = sp.track(track_id)
        titulo_spotify = str(track_info["name"])
        titulo_spotify1 = titulo_spotify.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
        print(titulo_spotify)
        res = requests.get(track_info["album"]["images"][0]["url"], stream=True)    
        with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
            shutil.copyfileobj(res.raw, out_file)
        with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
            img_data = img_file.read()
        results = Search(f"{track_info["name"]}, {track_info["album"]["artists"][0]["name"]}")
        if results.videos:
            while True:
                i = 0
                try:
                    results.videos[i].streams.get_audio_only().download(output_path=diretorio_destino)
                    titulo = results.videos[i].title
                except Exception as e:
                    i += 1  
                    break
            titulo_novo1 = titulo.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
            sound = AudioSegment.from_file(f"{diretorio_destino}/{titulo_novo1}.m4a", format="m4a")
            print(titulo_novo1)
            sound.export(f"{diretorio_destino}/{titulo_spotify1}.mp3", format="mp3")
            audiofile = eyed3.load(f"{diretorio_destino}/{titulo_spotify1}.mp3")
            if not audiofile.tag:
                audiofile.initTag()
            audiofile.tag.artist = track_info["album"]["artists"][0]["name"]
            audiofile.tag.images.set(3, img_data, "image/jpeg")
            audiofile.tag.save()
            os.remove(f"{diretorio_destino}/capa.jpg")
            os.remove(f"{diretorio_destino}/{titulo_novo1}.m4a")
if(__name__ == "__main__"):
    url = sys.argv[1]
    print("abaixando")
    if("youtu" in url):
        print("toutube")
        if(len(sys.argv) > 2):
            tipo = sys.argv[2]
            Download.Youtube(url=url, tipo=tipo)
    if("spotify" in url):
        print("spotify")
        Download.Spotify(url=url)