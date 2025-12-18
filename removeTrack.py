#ALL FILE NAMES MUST ENTIRELY USE ENGLISH CHARACETERS TO WORK (numbers and symbols are ok). (it might just be that the starting char must be in the english alphabet but remove all foreign characters to be sure).
#IF ^ ISN'T DONE THE TRACKS WILL BE MOVED OUT OF ORDER WITH NO ERROR MESSAGE OR WARNING

#CHANGE THE PATH CONSTANT AT THE BOTTOM BEFORE RUNNING

#If you think something is currently wrong with your tracknums, run the verify(PATH) subroutine, with PATH being the folder that contains the bad track numbers. It will print any errors to the terminal.

from mutagen.easyid3 import EasyID3 
import os

def check_access(dir):
    try:
        for name in os.listdir(dir):
            dire=dir+"/"+name
            audio=EasyID3(dire)
            audio.save()
    except:
        print(name, "cannot be accessed. Fix this before using this tool")
        return False
    
    return True

def del_track_from_dir(PATH, targetdir):
    allowed=check_access(PATH)

    if allowed:
        targetfile=EasyID3(targetdir)
        targetnum=int(targetfile["tracknumber"][0])

        os.remove(targetdir)

        try:
            file = open("deletedTracks.txt", "w")
            file.write(str(targetnum)+": "+targetdir[len(PATH)+1:-4])
            file.close()
        except:
            print(str(targetnum)+": "+targetdir[len(PATH)+1:-4])

        for name in os.listdir(PATH):
            if name[-3:]=="mp3":
                dire=PATH+"/"+name
                audio=EasyID3(dire)
                tracknum=int(audio["tracknumber"][0])
                if  tracknum > targetnum:
                    audio["tracknumber"] = str(tracknum - 1)
                    audio.save()
        verify(PATH)

def verify(PATH):
    allowed = check_access(PATH)
    if allowed:
        numCount={}
        for name in os.listdir(PATH):
            if name[-3:]=="mp3":
                dire=PATH+"/"+name
                audio=EasyID3(dire)
                tracknum=int(audio["tracknumber"][0])
                if tracknum in numCount:
                    numCount[tracknum]+=1
                    print(tracknum, "has been repeated. An error has occured")
                else:
                    numCount[tracknum]=1
        for i in range(1,max(numCount)+1):
            if i not in numCount:
                print(i, "has not been used as a track number. An error has occured")
    print("Verification complete")

if __name__ == "__main__":
    from tkinter import filedialog, Tk
    PATH = "C:/Users/ameli/Music/Yes!" #Change to the folder the song you want to remove is saved in. I could change this to another tkinter UI if that would be easier
    Tk().withdraw()
    dir = filedialog.askopenfilename(initialdir=PATH,filetypes=[("MP3 files", ".mp3")])
    if PATH in dir:
        del_track_from_dir(PATH,dir)