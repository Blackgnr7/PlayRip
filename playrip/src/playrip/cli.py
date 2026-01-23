from playrip import Dowload
import sys

def main():
    url = sys.argv[1]
    if("youtu" in url):
        print("\n------Abaixando video do Youtube------")
        if(len(sys.argv) > 2):
            tipo = sys.argv[2]
            Dowload.Youtube(url=url, formato_do_audio=tipo, thumbnail=True)
            return
    elif("spotify" in url):
        print("\n------Abaixando musica do spotify------")
        Dowload.Spotify(url=url, thumbnail=True)
        return
    else:
        print("\npf coloque um link no spotify ou youtube")
        return
