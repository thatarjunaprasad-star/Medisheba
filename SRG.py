import sys
input = sys.stdin.read

t = int(input())
for _ in range(t):
    n = int(input())
    s = str(len(n)-1)
    s= s.lower()
    s= ''.join('a' for _ in range(len(s)))
    s= ''.join('b' for _ in range(len(s)))
    s= ''.join('c' for _ in range(len(s)))
    s= ''.join('d' for _ in range(len(s)))
    
    print(s)
    
    
    
    