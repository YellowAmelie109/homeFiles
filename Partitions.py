#Partitions calculator
#n is the number being partitioned as an integer.
#p temporarily stores the currently being calculated partition as a list.
#app stores a partial partition when the subroutine calls itself for appending to p later as a list.
#parts stores every partition of n as a 2 dimensional list. Each dimension contains a value p has taken.
#counts tracks resticted partitions as a dictionary.
#k stores the user's choice for which largest part/number of parts restriction they want.

def sconjugate(parts,counts): #3rd called
    r=[]
    parts2=parts.copy()
    while len(parts2)>0:
        z=0
        r.append(len(parts2))
        for i in range(len(parts2)):
            parts2[i]=parts2[i]-1
            if parts2[i] == 0:
                z+=1
                
        for i in range(z):
            parts2.remove(0)
            
    if r == parts:
        counts["self"]+=1
        print("Self-conjugate")
        
    return counts

def disoddchk(p,counts): #4th called
#Assumes a partition is distinct and odd, until an even or repeated number is found.
    odd=True
    distinct=True
    for i in range(len(p)):
        if p[i]%2==0:
            odd=False
        if p.count(p[i])!=1:
            distinct=False
            
    if distinct and odd:
        print("All parts are odd and distinct")
        counts["disodd"]+=1
        counts["distinct"]+=1
        counts["odd"]+=1
    elif distinct:
        print("All parts are distinct")
        counts["distinct"]+=1
    elif odd:
        print("All parts are odd")
        counts["odd"]+=1
    return counts
    
def partitions(n,app,parts): #2nd called and recursive
    if n == 1:
        return [1]
    else:
        p=[1]*n
        if app==[]:
            parts.append(p.copy())
            
        while len(p)>1:
            if p.count(1)==0:
                app2=app.copy()
                for i in range(1,len(p)):
                    app2.append(p[i])
                partitions(p[0],app2,parts)
                
            p[-2]=p[-2]+1
            p[-1]=p[-1]-1
            for i in range(p.count(0)):
                p.remove(0)
                
            p2=p.copy()
            for i in range(len(app)):
                p2.append(app[i])
            parts.append(p2)
           
#Sort parts from highest to lowest and remove duplicate partitions.
#Must only run after all recurses to prevent the inclusion of incomplete partitions.
        if app==[]:
            newparts = []
            for i in range(len(parts)):
                parts[i].sort()
                parts[i].reverse()
#Remove duplicates
                if parts[i] not in newparts:
                    newparts.append(parts[i])
            newparts.sort()
            
            return newparts

def printArray(): #1st called
    counts={"odd":0, "distinct":0, "disodd":0, "self":0, "parts":[], "large":[]}
    n=int(input("Enter n: "))
    if n ==0:
        print("There is one partition of 0, being the empty sum")
    else:
        print()
        parts=partitions(n,[],[])
#Print every partition with information about which restrictions it is a part of.
        for i in range(len(parts)):
            pLen=len(parts[i])
            for j in range(pLen-1):
                print(parts[i][j],end="+")
            print(parts[i][-1])
                    
#Restricted partitions checks
            print(pLen, "parts")
            counts["parts"].append(pLen)
            
            print("Largest part is", parts[i][0])
            counts["large"].append(parts[i][0])
            
            counts=sconjugate(parts[i].copy(),counts)
            counts=disoddchk(parts[i],counts)
            print()

        k=int(input("Enter k: "))
        print()
#Outputs final results for all partition functions.
        print(f"Partitions of {n}: {len(parts)}")
        print(f"Partitions of {n} with exactly {k} parts: {counts['parts'].count(k)}")
        print(f"Partitions of {n} with largest part {k}: {counts['large'].count(k)}")
        print(f"Partitions of {n} whose parts are all odd: {counts['odd']}")
        print(f"Partitions of {n} whose parts are all distinct: {counts['distinct']}")
        print(f"Partitions of {n} that are self-conjugate: {counts['self']}")
        print(f"Partitions of {n} whose parts are all odd and distinct: {counts['disodd']}")

#Main code
printArray()
