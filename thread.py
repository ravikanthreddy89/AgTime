import sys;
import thread;
import time;

def manipulate(flag,data):
    print "Flag is :",flag;
    print "Data is :",data;

if __name__ =="__main__": 
    thread.start_new(manipulate, (1,12,));
    time.sleep(0.5);
    thread.start_new(manipulate,(2,13,));
    time.sleep(0.5);

