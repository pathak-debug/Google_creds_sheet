n = int(input())
a = list(map(int, input().split()))
for i in range(0,n):
    print(a[i]+(2*a[n-i-1]), end = " ")