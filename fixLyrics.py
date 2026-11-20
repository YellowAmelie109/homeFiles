rfile=open("oldlyrics.txt",'r')
wfile=open("newlyrics.txt",'w')
for line in rfile:
    done=False
    i=0
    while not done:
        if line[i]=='\n':
            done=True
        elif line[i]=="<" and (line[i-1]!=" " and line[i-1]!="]"):
            line=line[:i]+line[i+10:]
        i+=1
    
    wfile.write(line)
rfile.close()
wfile.close()
print("done")
