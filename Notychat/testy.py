# def solve(n,k, arr):
#     if k < n :
#         for i in range(n):
#             if i == k:
#                 temp = arr[i+1]
#                 arr[i+1] = arr[i]
#                 arr[i] = temp
#         count = 0
#         for i in range(n):
#             if i == k:
#                 temp = arr[i-1]
#                 sum = temp + arr[i]
#                 if sum %2 ==0:
#                     count = count + 1
#             if i > k:
#                 if arr[i]%2 ==0:
#                     count = count + 1
#         print(arr)
#         return count
# T= int(input())
# for _ in range(T):
#     n, k = map(int, input().split())
#     arr = list(map(int, input().split()))
#     out_ = solve(n, k, arr)
#     print (out_)

list = [1,2,3]
A = [i for i in list]
print(A)

