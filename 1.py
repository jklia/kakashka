flag = False
for a in range(0, 1000):
    for x in range(0, 100):
        if x % 13 != 0 or x % 21 == 0 or (x + a) >= 500:
            flag = True
        else:
            flag = False
            break
    if flag:
        print(a)
