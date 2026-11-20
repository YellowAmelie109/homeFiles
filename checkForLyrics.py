from mutagen.mp3 import MP3
import os
import re

PATH="/home/amelie/Music/Yes!/"

def checkForLyrics(audio):
            try:
                audio.tags['USLT:LYRICS:XXX']
                return True
            except:
                #print(audio.tags['TIT2'].pprint()[5:])
                return False

def checkForWordSync(audio):
    lyrics=audio.tags['USLT:LYRICS:XXX'].pprint()
    if re.search(r"<\d+:\d+\.\d+>",lyrics):# or lyrics[16:18]=="((":
        return True
    return False

nolyrics=[]
nowordsync=[]
for name in os.listdir(PATH):
        if name[-3:]=="mp3":
            audio=MP3(PATH+name)
            if checkForLyrics(audio):
                if not checkForWordSync(audio):
                    nowordsync.append(audio.tags['TIT2'].pprint()[5:])
            else:
                nolyrics.append(audio.tags['TIT2'].pprint()[5:])
nolyrics.sort()
nowordsync.sort()
print("\nNo lyrics:\n")
i=0
for song in nolyrics:
    i+=1
    print("{:>2}) {}".format(i,song))
print()
print("\nNo word sync:\n")
i=0
for song in nowordsync:
    i+=1
    print("{:>2}) {}".format(i,song))
