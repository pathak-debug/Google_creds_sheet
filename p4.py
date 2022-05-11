N = int(input())
a = list(map(int, input().split()))
k = int(input())
k = k-1
print(a[0])
print(a[3])
a = a.sort()
l = []

print(a)
for i in range(0,N):
    l.append(a[i])
print(l)