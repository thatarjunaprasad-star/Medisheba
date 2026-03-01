import os,sys

t = int(input())
for i in range(t):
    n = int(input())
    a = list(map(int,input().split()))
    b = list(map(int,input().split()))
    while True:
        mid= low+high//2
        low = mid+1
        high = mid-1
        if a[mid] == b[mid]:
            a[mid].swapcase(b[mid])
            break
    print(a)
    