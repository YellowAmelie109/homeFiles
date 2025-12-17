from mutagen.easyid3 import EasyID3 
import os
from tkinter import filedialog, Tk


def del_track_from_dir(PATH, targetdir):
    targetfile=EasyID3(targetdir)
    targetnum=int(targetfile["tracknumber"][0])
    os.remove(targetdir)

    for name in os.listdir(PATH):
        if name[-3:]=="mp3":
            dire=PATH+"/"+name
            audio=EasyID3(dire)
            tracknum=int(audio["tracknumber"][0])
            if  tracknum > targetnum:
                audio["tracknumber"] = str(tracknum - 1)
                audio.save()
        
if __name__ == "__main__":
    PATH = "C:/Users/ameli/Music/Yes!"
    Tk().withdraw()
    dir = filedialog.askopenfilename(initialdir=PATH,filetypes=[("MP3 files", ".mp3")])
    if PATH in dir:
        del_track_from_dir(PATH,dir)
        print("Deleted")
    