import sys
import thread;
import time;

def td_func():
    print "I am a new thread";


if __name__== "__main__":
    thread.start_new(td_func,());
    time.sleep(1);
    print "I am main thread";
    print sys.argv[1];
