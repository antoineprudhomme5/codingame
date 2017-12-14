input()
m=0
l=list(map(int,input().split()))
if l:m=min(l,key=abs)
print(m*-1 if(m<0 and abs(m)in l)else m)
