from multiprocessing import Process

def loop1(name):
    while True:
        print('hello', name)
def loop2():
    while True:
        print("x")
p = Process(target=loop1, args=('bob',)).start()
x = Process(target=loop2).start()
p.start()
x.start()
