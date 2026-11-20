#each func should only act within [] or <>, not on the whole line.
#fix before running half-sec funcs

def addHalfSecond(line):
        i=0
        for char in line:
            if char=="[" or char=="<":
                num=int(line[i+7])
                if num >4:
                    line=addSecond(line,i)
                    num-=5
                else:
                    num+=5
                line=line[:i+7]+str(num)+line[i+8:]
            i+=1
        return line

def subHalfSecond(line):
        i=0
        for char in line:
            if char=="[" or char=="<":
                num=int(line[i+7])
                if num <=4:
                    line=subSecond(line,i)
                    num+=5
                else:
                    num-=5
                line=line[:i+7]+str(num)+line[i+8:]
            i+=1
        return line
                    

def addSecond(line,pos=-1):
    if pos==-1:
        i=0
        for char in line:
            if char=="[" or char=="<":
                temp=int(line[i+5])+1
                if temp>9:
                    line=line[:i+5]+"0"+line[i+6:]
                    temp=int(line[i+4])+1
                    if temp>5:
                        line=line[:i+4]+"0"+line[i+5:]
                        temp=int(line[i+2])+1
                        line=line[:i+2]+str(temp)+line[i+3:]
                    else:
                        line=line[:i+4]+str(temp)+line[i+5:]
                else:
                    line=line[:i+5]+str(temp)+line[i+6:]
            i+=1
    else:
        i=pos
        temp=int(line[i+5])+1
        if temp>9:
            line=line[:i+5]+"0"+line[i+6:]
            temp=int(line[i+4])+1
            if temp>5:
                line=line[:i+4]+"0"+line[i+5:]
                temp=int(line[i+2])+1
                line=line[:i+2]+str(temp)+line[i+3:]
            else:
                line=line[:i+4]+str(temp)+line[i+5:]
        else:
            line=line[:i+5]+str(temp)+line[i+6:]
    return line

def subSecond(line,pos=-1):
    if pos==-1:
        i=0
        for char in line:
            if char=="[" or char=="<":
                temp=int(line[i+5])-1
                if temp<0:
                    line=line[:i+5]+"9"+line[i+6:]
                    temp=int(line[i+4])-1
                    if temp<0:
                        line=line[:i+4]+"5"+line[i+5:]
                        temp=int(line[i+2])-1
                        line=line[:i+2]+str(temp)+line[i+3:]
                    else:
                        line=line[:i+4]+str(temp)+line[i+5:]
                else:
                    line=line[:i+5]+str(temp)+line[i+6:]
            i+=1
    else:
        i=pos
        temp=int(line[i+5])-1
        if temp<0:
            line=line[:i+5]+"9"+line[i+6:]
            temp=int(line[i+4])-1
            if temp<0:
                line=line[:i+4]+"5"+line[i+5:]
                temp=int(line[i+2])-1
                line=line[:i+2]+str(temp)+line[i+3:]
            else:
                line=line[:i+4]+str(temp)+line[i+5:]
        else:
            line=line[:i+5]+str(temp)+line[i+6:]
    return line
    
def loop(length,addorsub):
    if length == "s" and addorsub=="a":
        for line in rfile:
            line=addSecond(line)
            wfile.write(line)
        print("added a second")
    elif length=="s" and addorsub=="s":
        for line in rfile:
            line=subSecond(line)
            wfile.write(line)
        print("subbed a second")
    elif length=="h" and addorsub=="a":
        for line in rfile:
            line=addHalfSecond(line)
            wfile.write(line)
        print("added half a second")
    elif length=="h" and addorsub=="s":
        for line in rfile:
            line=subHalfSecond(line)
            wfile.write(line)
        print("subbed half a second")
    else:
        print("bad inputs")

rfile = open("oldlyrics.txt", 'r')
wfile = open("newlyrics.txt", 'w')

length=input("second (s) or half-second (h): ")
addorsub=input("add (a) or sub (s): ")
loop(length,addorsub)

rfile.close()
wfile.close()

