from time import *
timer1 = time()
sleep(4)
list = []
for i in range(1, 1000):
    for j in range(i):
        list.append(j**22)
timer2 = time()
print(timer2-timer1, (timer2-timer1)%1)