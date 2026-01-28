import requests
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os
from pydub import AudioSegment
from pytubefix import Search, YouTube
import logging

logging.getLogger("spotipy").setLevel(logging.CRITICAL)
client_id = "82190b6d4e6d4250a7e8d5a16a29443c"
client_secret = "eb3c7e469f40400b941dc05116cfc55b"


def id(url):
    if("youtu" in url):
        patterns = [r"(?:youtu\.be/)([^?&]+)", r"(?:v=)([^?&]+)"]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    elif("spotify" in url):
        track_id = url.split("/track/")[1].split("?")[0]
        return track_id
    else:
        return None


def thumbnail(url, diretorio_destino):
    if "spotify" in url:
        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        track_info = sp.track(url)
        res = requests.get(track_info["album"]["images"][0]["url"], stream=True)
        with open(f"{diretorio_destino}/capa.jpg", "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
        try:
            os.remove(".cache")
        except Exception as e:
            pass
    if "youtu" in url:
        codigo = id(url=url)
        thumbnail_para_abaixar = (
            "https://i.ytimg.com/vi_webp/" + codigo + "/maxresdefault.webp"
        )
        res = requests.get(thumbnail_para_abaixar, stream=True)
        with open(f"{diretorio_destino}/capa.jpg", "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)


def audio(url, diretorio_destino):
    if "spotify" in url:
        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        track_info = sp.track(url)
        Novo_titulo_spotify = (
            str(track_info["name"])
            .replace("/", "")
            .replace("|", "")
            .replace("?", "")
            .replace("*", "")
            .replace("<", "")
            .replace(">", "")
            .replace(":", "")
            .replace("\\", "")
        )
        results = Search(
            f"{track_info["name"]}, {track_info["album"]["artists"][0]["name"]}"
        )
        if results.videos:
            while True:
                i = 0
                try:
                    results.videos[i].streams.get_audio_only().download(
                        output_path=diretorio_destino
                    )
                    titulo = results.videos[i].title
                except Exception as e:
                    i += 1
                else:
                    break
            titulo_novo1 = (
                titulo.replace("/", "")
                .replace("|", "")
                .replace("?", "")
                .replace("*", "")
                .replace("<", "")
                .replace(">", "")
                .replace(":", "")
                .replace("\\", "")
            )
            os.rename(f"{diretorio_destino}/{titulo_novo1}.m4a", f"{diretorio_destino}/{Novo_titulo_spotify}.m4a")
            sound = AudioSegment.from_file(
                f"{diretorio_destino}/{Novo_titulo_spotify}.m4a", format="m4a"
            )
            sound.export(f"{diretorio_destino}/{Novo_titulo_spotify}.mp3", format="mp3")
            os.remove(f"{diretorio_destino}/{Novo_titulo_spotify}.m4a")
            try:
                os.remove(".cache")
            except Exception as e:
                pass
    if "youtu" in url:
        yt = YouTube(url)
        titulo = yt.title
        titulo_novo1 = (
            titulo.replace("/", "")
            .replace("|", "")
            .replace("?", "")
            .replace("*", "")
            .replace("<", "")
            .replace(">", "")
            .replace(":", "")
            .replace("\\", "")
        )
        caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.m4a"
        yt.streams.get_audio_only().download(output_path=diretorio_destino)
        sound = AudioSegment.from_file(caminho_arquivo, format="m4a")
        sound.export(f"{diretorio_destino}/{titulo_novo1}.mp3", format="mp3")
        os.remove(f"{diretorio_destino}/{titulo_novo1}.m4a")


def video(url, diretorio_destino):
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download(output_path=diretorio_destino)