from mutagen.mp3 import MP3
import os


def audio_duration(length):
    hours = int(length // 3600)
    length %= 3600
    mins = int(length // 60)
    length %= 60
    seconds = int(round(length,0))

    return hours, mins, seconds

if __name__ == "__main__":
    PATH = "C:/Users/ameli/Music/Yes!"
    length=0
    for name in os.listdir(PATH):
        if name[-3:]=="mp3":
            dire=PATH+"/"+name
            audio=MP3(dire)
            length+=audio.info.length
    hours, mins, seconds = audio_duration(length)
    print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))
