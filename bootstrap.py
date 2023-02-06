#to run python3 [servername] [path]
import os
import time
import threading
import random
import sys
from threading import *

#CENTRAL SERVER
MAXTIMEOUT=3
SREQ="./server_req/"
SRES="./server_res/"
CREQ="./client_req/"
CRES="./client_res/"
COUNT=1
obj = Semaphore(1)
nargs = len(sys.argv)
if(nargs<3):
    print("[-]Invalid Details")
    quit()
else:
    if(not os.path.exists(sys.argv[2]+"/"+sys.argv[1])):
        os.mkdir(sys.argv[2]+"/"+sys.argv[1])
    os.chdir(sys.argv[2]+"/"+sys.argv[1])
    if(not os.path.exists("server_req")):
        os.mkdir("server_req")
    if(not os.path.exists("server_res")):
        os.mkdir("server_res")
    f=open("sdetails.txt","w");
    f.close();


THREADPOOL=2

def serve_req(req,s_details):
    print("serving")
    obj.acquire()
    global COUNT
    global THREADPOOL
    server_name="SV"+str(COUNT)
    COUNT=COUNT+1
    obj.release()
    det=server_name+" "+s_details[0].strip()+" "+s_details[1].strip()+" "+s_details[2].strip()+"\n"
    print(det)
    with open(SRES+"/"+req,"w") as res_f:
        res_f.write(server_name)
    with open("sdetails.txt","a") as f:
        f.write(det)
    obj.acquire()
    THREADPOOL+=1
    obj.release()
    print(THREADPOOL)
    

#server requests
while(True):
    fnames=os.listdir(SREQ)
    print("Running..")
    print(THREADPOOL)
    for req in fnames:
        timer=0
        while(True):
            if(THREADPOOL>0):
                s_details=None
                with open(SREQ+"/"+req) as f:
                    s_details=f.readlines();
                    print(s_details)
                os.remove(SREQ+"/"+req)
                THREADPOOL=THREADPOOL-1
                thread1=threading.Thread(target=serve_req,args=(req,s_details))
                thread1.start()
                break
            
            else:
                timer+=1
                if(timer>MAXTIMEOUT):
                    print("[-]Timeout expired")
                    break
        

    time.sleep(2)


