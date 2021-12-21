import time

li = [i for i in range(100000000)]

#method 1
start1 = time.perf_counter()

rli1 = li[::-1]

end1 = time.perf_counter()
print(rli1[:5])

print('Time for method 1: ' + str(end1-start1))

#method 2
start2 = time.perf_counter()

rli2 = list(reversed(li))

end2 = time.perf_counter()
print(rli2[:5])

print('Time for method 2: ' + str(end2-start2))

#method 3

start3 = time.perf_counter()

rli3 = []
for item in reversed(li):
    rli3.append(item)

end3 = time.perf_counter()

print(rli3[:5])

print('Time for method 3: ' + str(end3-start3))

#method 4

start4 = time.perf_counter()

rli4 = li[:]
rli4.reverse()

end4 = time.perf_counter()

print(rli4[:5])

print('Time for method 4: ' + str(end4-start4))





