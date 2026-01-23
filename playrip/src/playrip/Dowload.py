import os
from mutagen.mp4 import MP4, MP4Cover
from playrip import get
import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytubefix import YouTube
import logging  

logging.getLogger("spotipy").setLevel(logging.CRITICAL)
diretorio_destino = os.path.expanduser("~/Downloads")
client_id = "82190b6d4e6d4250a7e8d5a16a29443c"
client_secret = "eb3c7e469f40400b941dc05116cfc55b"


def Youtube(url, formato_do_audio, thumbnail):
    if formato_do_audio.lower() == "mp3":
        yt = YouTube(url)
        artist = yt.author
        titulo = yt.title
        print(f"titulo do video do Youtube: {titulo}")
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
        get.audio(url=url,diretorio_destino=diretorio_destino)
        audiofile = eyed3.load(f"{diretorio_destino}/{titulo_novo1}.mp3")
        if not audiofile.tag:
            audiofile.initTag()
        audiofile.tag.artist = artist
        if thumbnail:
            get.thumbnail(url=url,info=None,diretorio_destino=diretorio_destino)
            with open(f"{diretorio_destino}/capa.jpg", "rb") as img_file:
                img_data = img_file.read()
            audiofile.tag.images.set(3, img_data, "image/jpeg")
        audiofile.tag.save()
        os.remove(f"{diretorio_destino}/capa.jpg")
        os.remove(f"{caminho_arquivo}")
    if formato_do_audio.lower() == "mp4":
        yt = YouTube(url)
        artist = yt.author
        titulo = yt.title
        print(f"titulo do video do Youtube: {titulo}")
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
        get.video(url=url,diretorio_destino=diretorio_destino)
        caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.mp4"
        video = MP4(caminho_arquivo)
        video["\xa9ART"] = artist
        if thumbnail:
            get.thumbnail(url=url,info=None,diretorio_destino=diretorio_destino)
            with open(f"{diretorio_destino}/capa.jpg", "rb") as img_file:
                img_data = img_file.read()
            video["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
        video.save()
        os.remove(f"{diretorio_destino}/capa.jpg")

def Spotify(url, thumbnail):
    auth_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    track_info = sp.track(url)
    titulo_spotify = str(track_info["name"])
    Novo_titulo_spotify = (
        titulo_spotify.replace("/", "")
        .replace("|", "")
        .replace("?", "")
        .replace("*", "")
        .replace("<", "")
        .replace(">", "")
        .replace(":", "")
        .replace("\\", "")
    )
    print(f"titulo da musica do spotify: {titulo_spotify}\n")
    get.audio(url=url, diretorio_destino=diretorio_destino)
    audiofile = eyed3.load(f"{diretorio_destino}/{Novo_titulo_spotify}.mp3")
    if not audiofile.tag:
        audiofile.initTag()
    audiofile.tag.artist = track_info["album"]["artists"][0]["name"]
    if thumbnail:
        get.thumbnail(url=url, info=track_info, diretorio_destino=diretorio_destino)
        with open(f"{diretorio_destino}/capa.jpg", "rb") as img_file:
            img_data = img_file.read()
        audiofile.tag.images.set(3, img_data, "image/jpeg")
    audiofile.tag.save()
    os.remove(f"{diretorio_destino}/capa.jpg")
    os.remove(f"{diretorio_destino}/{Novo_titulo_spotify}.m4a")
    try:
        os.remove(".cache")
    except Exception as e:
        pass
