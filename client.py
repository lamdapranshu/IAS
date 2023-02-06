import ftplib
import os
import time
import threading
import random
import sys
from threading import *

#PATHS
SERVE_FILE="sdetails.txt"
SREQ="./requests"
SRES="./responses"
PARENT="./../"
RESPONSE="/responses"
S_D={}
STATE={}
NAME=""
MAXTIMEOUT=5
MIP="127.1.1.1"
MPORT=2121
F=["add","sub","mul","div","plusplus"]
#FUNCTIONS
def makefolder(NAME):
    os.mkdir(NAME)
    os.chdir("./"+NAME)

def welcome():
    print("Welcome!")
    time.sleep(1)
    print("[*]FTP Messaging App")

def randN(N):
	min = pow(10, N-1)
	max = pow(10, N) - 1
	return random.randint(min, max)

def process_server_details():
    with open(SERVE_FILE,"r") as f:
        det=f.readlines();
        for d in det:
            print(d)
            d=d.split()
            print(d)
            S_D[d[0]]=d 
        print(S_D)
def download_file(ftp,tfn):
    with open(tfn, "wb") as file:
        retCode = ftp.retrbinary("RETR " + tfn, file.write)
        return tfn
def lookup(mftp):
    if os.path.exists(SERVE_FILE):
        os.remove(SERVE_FILE)
    download_file(mftp,SERVE_FILE);
    process_server_details()
def extract_details(filename):
    flist=[]
    temp=""
    for i in filename:
        if(i=="$"):
            flist.append(temp)
            temp=""
        else:
            temp=temp+i
    flist.append(temp)
    return flist


def send_message(nums,func,server):
    uid=randN(8)
    global NAME
    print(NAME,func,uid)
    func=func-1
    req_file_name=NAME+"$"+F[func]+"$"+str(uid)
    with open(req_file_name,"w") as file:
        file.write(str(nums)+"\n");
        if S_D.get(server) is not None:
            if STATE.get(server) is not None:
                file.write(STATE[server])
        else:
            print("Invalid Server Name")
            return
    ftp = ftplib.FTP(timeout=30)
    ftp.connect(S_D[server][2], int(S_D[server][3]))
    ftp.login()
    with open(req_file_name, "rb") as f:
        ftp.cwd(SREQ)
        ftp.storbinary(f"STOR {req_file_name}", f, blocksize=1024*1024)
        ftp.cwd(PARENT)
    os.remove(req_file_name)
    print("[+]Trying to fetch response")
    ftp.cwd(RESPONSE)
    time.sleep(5)
    timer=0
    received=False
    while(True):
        
        fnames=ftp.nlst()
        print(fnames)
        for i in fnames:
            print(i)
            flist=extract_details(i)
            sender=flist[0]
            id=flist[2]
            print(NAME)
            print(uid)
            if(sender==NAME and id==str(uid)):
                download_file(ftp,i)
                status=ftp.delete(i)
                file= open(i, "r")
                con=file.readlines()
                if(len(con)>1):
                    if(con[0]=="FE"):
                        print("Invalid function")
                    elif(con[0]=="SE"):
                        print("Session ID invalid")
                        del STATE[server]
                    else:
                        print(con[0])
                        STATE[server]=int(con[1])

                file.close()
                os.remove(i)
                received=True

        if(received): break
        else: 
            timer+=1
            time.sleep(2)
            if(timer>MAXTIMEOUT):
                print("[+]Timelimit expired")
                break
    


if __name__=="__main__":
    welcome()
    print("[*]Enter your Name")
    NAME=input()
    makefolder(NAME)
    mftp = ftplib.FTP(timeout=30)
    mftp.connect(MIP, MPORT)
    mftp.login()
    lookup(mftp)
    while(1):
        print("[+]Enter the operation you want to perform. Enter number")
        print("[+]1. Lookup")
        print("[+]2. Send Message")
        n=int(input())
        if(n==1):
            lookup(mftp)
        elif(n==2):
            func=int(input("[+]Enter the operation code\n1. Add\n2. Sub\n3. Multiply\n4. Div\n5. PlusPlus\n"))
            if(func<0 and func>6):
                print("innvalid function")
                continue
            print("Enter space seperated nums. if operation is plusplus then enter none\n")
            nums=input()
            print("Enter servername you want to direct this operation to\n")
            server=input()
            send_message(nums,func,server)
