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
        print(name, "cannot be accessed. Fix this before using this tool\n")
        return False
    
    return True

def del_track_from_dir(PATH, targetdir):
    allowed=check_access(PATH)

    if allowed:
        targetfile=EasyID3(targetdir)
        targetnum=int(targetfile["tracknumber"][0])

        os.remove(targetdir)

        try:
            file = open("deletedTracks.txt", "a")
            file.write(str(targetnum)+": "+targetdir[len(PATH)+1:-4]+'\n')
            file.close()
        finally:
            print("Deleted num "+str(targetnum)+": "+targetdir[len(PATH)+1:-4]+'\n')

        for name in os.listdir(PATH):
            if name[-3:]=="mp3":
                dire=PATH+"/"+name
                audio=EasyID3(dire)
                tracknum=int(audio["tracknumber"][0])
                if  tracknum > targetnum:
                    audio["tracknumber"] = str(tracknum - 1)
                    audio.save()
    return allowed

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
                    print(tracknum, "has been repeated. An error has occured\n")
                else:
                    numCount[tracknum]=1
        for i in range(1,max(numCount)+1):
            if i not in numCount:
                print(i, "has not been used as a track number. An error has occured\n")
    print("Verification complete\n")

if __name__ == "__main__":
    from tkinter import filedialog, Tk
    PATH = "" #Change to the folder the song you want to remove is saved in. I could change this to another tkinter UI if that would be easier
    Tk().withdraw()
    dir = filedialog.askopenfilenames(initialdir=PATH,filetypes=[("MP3 files", ".mp3")])
    needsVerification=False
    if len(dir)>0:
        print()
        for track in dir:
            if PATH in track:
                deleted=del_track_from_dir(PATH,track)
                if not needsVerification and deleted:
                    needsVerification = True
            else:
                print("Change the PATH constant to select a different folder\n")
        if needsVerification:
            verify(PATH)