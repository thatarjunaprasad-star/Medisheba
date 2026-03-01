import sys

t =  int(input())
for i in range(t):
    h = int(input())
    n = int(input())
    a = list(map(int,input().split()))
    k = int(input())
    def kill():
        i=0
        while(i<h):
            h= h- a[i]
            i+=1
            if h<= n*a[i]:
                k=-1
                z=min(0,k)        
        
        return z              

            

    
    print(kill())