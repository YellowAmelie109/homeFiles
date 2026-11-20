import os
from mutagen.easyid3 import EasyID3

if __name__ == "__main__":
    dPATH = "/home/amelie/Music/Download/"
    yPATH = "/home/amelie/Music/Yes!/"
    num=0
    for name in os.listdir(yPATH):
        if name[-3:]=="mp3":
            num+=1
    addnum=1
    for name in os.listdir(dPATH):
        if name[-3:]=="mp3":
            dire=dPATH+"/"+name
            audio=EasyID3(dire)
            i=addnum+num
            addnum+=1
            audio["tracknumber"] = str(i)
            audio.save()
            os.rename(dire,yPATH+"/"+name)
    print(f"Added {addnum-1} tracks")
