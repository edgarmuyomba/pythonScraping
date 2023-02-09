import _thread 
import time 

def printLine(max, delay):
    for i in range(0, max):
        time.sleep(delay)
        print(i)
        i += 1


def main():
    js = [1,2,3,4,5]
    for j in js:
        _thread.start_new_thread(printLine, (j, 3))
        _thread.start_new_thread(printLine, (j, 5))

if __name__ == '__main__':
    main()