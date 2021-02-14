import time
start = time.time()
for i in range(5):
    print("hello")
    time.sleep(1)
print ("it took {time} econds".format(time = time.time() - start))
