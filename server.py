import ftplib
import os
import time
import threading
import random
import sys
from threading import *

#--------------------------------------------------------------------------
#AUTOMATE DIR CREATION
nargs = len(sys.argv)
if(nargs<3):
    print("[-]Invalid Details")
    quit()
else:
    os.mkdir(sys.argv[2]+"/"+sys.argv[1])
    os.chdir(sys.argv[2]+"/"+sys.argv[1])
    os.mkdir("requests")
    os.mkdir("responses")
    
#MASTER SERVER CREDENTIALS
MIP="127.1.1.1"
MPORT=2121
DIR_REQ="./server_req"
DIR_RES="./server_res"
PARENT="./.."
ftp=None
#MY FTP CREDENTIALS
MYIP=None
MYPORT=None
SERVERNAME=None
#MY DIR PATH
REQUEST="./requests/"
RESPONSE="./responses/"
PARENT="/../"
#CONSTANTS
MAXTIMEOUT=10
#SETTING SESSIONS IF REQUIRED
SESS={}
#HANDLING CLIENT REQUEST
THREAD_POOL=4
#DECLARING GLOBAL VARIABLES AND TAKING REQUIREMENTS
FUNC={"ADD":False,"SUB":False,"MUL":False,"DIV":False,"PLUSPLUS":False}
FUNC_NAME=["ADD","SUB","MUL","DIV","PLUSPLUS"]
F=["add","sub","mul","div","plusplus"]
S_REQ=False
obj = Semaphore(1)
#FUNCTIONS
def randN(N):
	min = pow(10, N-1)
	max = pow(10, N) - 1
	return random.randint(min, max)
def add(a,b):
    response=None
    try:
        response=int(a)+int(b)
    except Exception as e:
        response=e
        print(e)
    return response
def multiply(a,b):
    response=None
    try:
        response=int(a)*int(b)
    except Exception as e:
        response=e
        print(e)
    return response
def divide(a,b):
    response=None
    try:
        response=int(a)/int(b)
    except Exception as e:
        response=e
        print(e)
    return response
def sub(a,b):
    response=None
    try:
        response=int(a)-int(b)
    except Exception as e:
        response=e
        print(e)
    return response
def plusplus(a):
    response=None
    try:
        response=int(a)+1
    except Exception as e:
        response=e
        print(e)
    return response
def download_file(ftp,tfn):
    with open(tfn, "wb") as file:
        retCode = ftp.retrbinary("RETR " + tfn, file.write)
    return tfn

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
def process_request(c_req,content):
    output=None
    curr_session=None
    sessioned_output=None
    global THREAD_POOL
    flist=extract_details(c_req)
    #UNPACKING VALUES
    try:
        print(flist)
        sender=flist[0].strip()
        funct=flist[1].strip()
        id=flist[2].strip()
    except Exception as e:
        print("[-]Error Occured while processing the name of the file:- ",e)
        obj.acquire()
        THREAD_POOL+=1
        obj.release()
        return
    try:

        print(funct)
        if FUNC[FUNC_NAME[F.index(funct)]]:
            numbers=content[0].split()
            if(FUNC[FUNC_NAME[4]]):
                if(len(content)>1):
                    curr_session=int(content[1])
                    if SESS.get(curr_session) is not None:
                        sessioned_output=SESS[curr_session]
                    else:
                        print("[-]Invalid Session Id")
                        output="I"
                else:
                    while(True):
                        curr_session=randN(8)
                        if SESS.get(curr_session) is None:
                            break
        else:
            output="F"
            print("[-]Not a valid function for server")
        if(output=="F"):
            output="FE"
        elif(output=="S"):
            output="SE"
        else:
            if(funct=="add"):
                output=add(numbers[0],numbers[1])
            elif(funct=="sub"):
                output=sub(numbers[0],numbers[1])
            elif(funct=="div"):
                output=divide(numbers[0],numbers[1])
            elif(funct=="mul"):
                output=multiply(numbers[0],numbers[1])
            elif(funct=="plusplus"):
                output=plusplus(sessioned_output)
        if(FUNC[FUNC_NAME[4]]):
            SESS[sessioned_output]=output
    except Exception as e:
        print("[-]Error occured while processing request file of a clien:- ",e)
        obj.acquire()
        THREAD_POOL+=1
        obj.release()
        return
    #UPLOAD THE RESPONSE
    try:
        with open(RESPONSE+c_req,"w") as c_res:
            c_res.write(str(output))
            if(sessioned_output is not None):
                c_res.write("\n"+str(sessioned_output))
    except Exception as e:
        print("[-]Error occured while uploading the file:- "+e)
        obj.acquire()
        THREAD_POOL+=1
        obj.release()
        return
    obj.acquire()
    THREAD_POOL+=1
    obj.release()
    
            


#REGISTER SERVER
try:

    while(True):
        print("[+]Type Number of the functions. You want to include in server")
        print("[+]1. 0->ADDITION\n2. 1->SUBSTRACTION\n3. 2->MULTIPLICATION\n4. 3->DIVISION\n 5. 4->PLUSPLUS\n 6. 5->continue")
        check=False
        while(True):
            print("[+]Give one input")
            print("[.]",end='')
            in1=input()
            try:
                if(int(in1)>5 or int(in1)<0):
                    print("[-]Invalid Input")
                    continue
                elif(int(in1)==5): break
                else:
                    FUNC[FUNC_NAME[int(in1)]]=True
                    check=True
            except Exception as e:
                print("[-]Invalid Inputplease enter a valid code:- ",e)

        if(check):
            break
        else:
            print("[*]Atleast one functionality should be there")

    #TAKE A TEMP NAME
    while(True):
        NAME=input("[+]Enter a Name")
        print("[.]",end='')
        if(len(NAME) and NAME.isalpha()):
            NAME+=str(randN(4))
            break
        else:
            print("[-]Invalid input. Should only contain Alphabet")
            continue
    #TAKE SERVER'S FTP CREDENTIALS
    while(True):
        MYIP=input("[+]Enter IP of your server")
        MYPORT=int(input("[+]Enter port no. for your server"))
        if(MYIP and MYPORT):
            break
   #MAKING REQ FILE AND REGISTERING ON MASTER SERVER     
    try:
        with open("req.txt","w") as req_file:
            req=""
            for i in FUNC_NAME:
                if(FUNC[i]):
                    req+="1"
                else:
                    req+="0"
            req_file.write(str(req)+"\n")
            req_file.write(str(MYIP)+"\n")
            req_file.write(str(MYPORT))

    except Exception as e:
        print("[-]Error while making requirement file:-  ",e)
        quit()
    
    #ESTABLISHING CONNECTION
    try:
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(MIP, MPORT)
        ftp.login()
        print("[+]Successfully Connected to Central server")
    except Exception as e:
        print(e)
        print("[-]Some error occured while establishing connection")
        quit()
    #REGISTERING ON CENTRAL SERVER
    try:
        try:
            with open("req.txt", "rb") as req_file:
                ftp.cwd(DIR_REQ)
                ftp.storbinary(f"STOR {NAME}", req_file, blocksize=1024*1024)
                ftp.cwd(PARENT)
        except Exception as e:
            print("[-]Failed to upload the requirement file:- ",e)
            quit()
        print("[*]Wait trying to establish connection")
        time.sleep(2)
        try:
            rattempts=0
            dstatus=None
            reg_succ=False
            ftp.cwd(DIR_RES)
            while(True):
                requests=ftp.nlst()
                for request in requests:
                    if(request==NAME):
                        download_file(ftp,request)
                        dstatus=ftp.delete(request)
                        with open(NAME,"r") as d_file:
                            SERVERNAME=d_file.read()
                            print("[+]Register request have been accepted")
                            print("[+]Server Id:-",SERVERNAME)
                        os.remove(NAME)
                        reg_succ=True

                if(reg_succ):
                    break
                if(rattempts>3):
                    print("[-]No Response from the server failed to register")
                    print("[-]Closing the application..")
                    quit() 
                time.sleep(2)
            ftp.cwd(PARENT)          
        except Exception as e:
            print("[-]Error Occured while registering on the server:-",e)
            print("[-]Status download:-",dstatus)
    except Exception as e:
            print("[-]Error Occured while registering on the server(CENTRAL SERVER TRY):- ",e)

    print("[+]REGISTERATION COMPLETE")
    print(FUNC)
    while(True):
        #SERVE REQUEST FOR OTHERS
        fnames=os.listdir(REQUEST)
        for c_req in fnames:
            timer=0
            while(True):
                if(THREAD_POOL>0):
                    THREAD_POOL=THREAD_POOL-1
                    content=None
                    with open(REQUEST+"/"+c_req,"r") as file:
                        content=file.readlines()
                    os.remove(REQUEST+"/"+c_req)
                    thread1=threading.Thread(target=process_request,args=(c_req,content))
                    thread1.start()
                    break
                else:
                    print("[^]Experiancing overload")
                    timer+=2
                    time.sleep(1)
                    if(time>MAXTIMEOUT):
                        print("[-]Timed Out")
                        break
        time.sleep(2)

except Exception as e:
    print(e)