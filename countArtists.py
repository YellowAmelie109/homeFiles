from mutagen.mp3 import MP3
import os

if __name__ == "__main__":
    PATH = "/home/amelie/Music/Yes!/"
    artists=dict()
    for name in os.listdir(PATH):
        if name[-3:]=="mp3":
            dire=PATH+"/"+name
            audio=MP3(dire)
            artist=audio.tags["TPE1"].pprint()[5:]
            if artist in artists:
                artists[artist]+=1
            else:
                artists[artist]=1
    pos=1
    count=0
    last=0
    length=len(str(len(artists)))
    for key in sorted(artists, key=artists.get, reverse=True):
        count+=1
        if artists[key]<last:
            pos+=1
        last=artists[key]
        print(f"{f"{pos}/{count}":>{length*2+1}}) {key}: {artists[key]}")
        
