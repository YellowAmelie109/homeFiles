import time
bees=open("bees.txt",'r')
while True:
    time.sleep(1)
    text=bees.read(2000)
    print(text)
    if len(text)<2000:
        break
bees.close()
