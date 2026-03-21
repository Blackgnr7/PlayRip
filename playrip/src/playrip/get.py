import requests
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os
from pydub import AudioSegment
from pytubefix import Search, YouTube
import subprocess


def id(url):
    if "youtu" in url:
        patterns = [r"(?:youtu\.be/)([^?&]+)", r"(?:v=)([^?&]+)"]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    elif "spotify" in url:
        track_id = url.split("/track/")[1].split("?")[0]
        return track_id
    else:
        return None


def thumbnail(diretorio_destino, url):
    if "i.scdn.co" in url:
        res = requests.get(url, stream=True)
        with open(f"{diretorio_destino}/capa.jpg", "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
    if "youtu" in url:
        codigo = id(url=url)
        thumbnail_para_abaixar = (
            "https://i.ytimg.com/vi_webp/" + codigo + "/maxresdefault.webp"
        )
        res = requests.get(thumbnail_para_abaixar, stream=True)
        with open(f"{diretorio_destino}/capa.jpg", "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)


def audio(diretorio_destino, url=None, artista=None, titulo_da_musica=None):
    if url == None:
        results = Search(f"{titulo_da_musica}, {artista}")
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
            os.rename(
                f"{diretorio_destino}/{titulo_novo1}.m4a",
                f"{diretorio_destino}/{titulo_da_musica}.m4a",
            )
            sound = AudioSegment.from_file(
                f"{diretorio_destino}/{titulo_da_musica}.m4a", format="m4a"
            )
            sound.export(f"{diretorio_destino}/{titulo_da_musica}.mp3", format="mp3")
            os.remove(f"{diretorio_destino}/{titulo_da_musica}.m4a")
            try:
                os.remove(".cache")
            except Exception as e:
                pass
    elif "youtu" in url:
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
    video = (
        yt.streams.filter(progressive=False, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )
    audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
    video.download(filename="video.mp4", output_path=diretorio_destino)
    audio.download(filename="audio.mp4", output_path=diretorio_destino)
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            f"{diretorio_destino}/video.mp4",
            "-i",
            f"{diretorio_destino}/audio.mp4",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            f"{diretorio_destino}/{titulo_novo1}.mp4",
        ]
    )
    os.remove(f"{diretorio_destino}/audio.mp4")
    os.remove(f"{diretorio_destino}/video.mp4")
