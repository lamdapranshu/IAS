import ftplib
import os
import time
import threading
import random

print("Welcome!")
time.sleep(1)
print("[*]FTP Messaging App")

#Message format
# Name of sender
# message

#Global Variables
mcount=1
master_file="master_file"
mycount=0

while(1):

    #make these also dynamic
    print("[*]Enter URL or IP")
    ftpHost = "127.1.1.1"
    print("[*]Enter Port No.")
    ftpPort = 2121
    print("Enter your Name")
    Name=input()
    # ftpUname = "username"
    # ftpPass = "password"



        

    #connection establishment
    try:
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(ftpHost, ftpPort)
        ftp.login()
        print("[+]Successfully Connected to server")
    except Exception as e:
        print(e)
        print("[-]Some error occured while establishing connection")
        quit()

    def download_file(ftp,tfn):
        a=""
        l=[]
        for i in range(len(tfn)):
            if tfn[i]=="/":
                l.append(a)
                a=""
            else:
                a+=tfn[i]
        path=""
        if(len(a)==len(tfn)):
            path="/"
        else: path=tfn[:(len(tfn)-len(a))-1]
        # print(path)
        # print(a)
        ftp.cwd(path)
        with open(a, "wb") as file:
            retCode = ftp.retrbinary("RETR " + a, file.write)
        ftp.cwd("/")
        # print("done")
        return a

    def send_message(ftp):
        print("Press 1 to send message")
        if(input()!="1"): return
        print("Enter Receiver Name")
        r=input()
        print("Enter Message")
        m=input()
        fnames=ftp.nlst()
        if r in fnames:
            download_file(ftp,r)
            # print("download done")
            f=open(r, "w")
            sa=Name+": "+m   
            f.write(sa)
            f.close()
            # print("write done")
            with open(r, "rb") as f:
                ftp.storbinary(f"STOR {r}", f, blocksize=1024*1024)
            # print("ok")
            os.remove(r)
        else:
            # print("here")
            f=open(r, "w")
            sa=Name+": "+m   
            f.write(sa)
            f.close()
            # print("write done")
            try:
                with open(r, "rb") as f:
                    ftp.storbinary(f"STOR {r}", f, blocksize=1024*1024)
            except Exception as e:
                print(e)
            os.remove(r)
            # print("ok")
            

    def get_messgae():
        # print("Fetching Messages")
        fnames=ftp.nlst()
        if Name in fnames:
            download_file(ftp,Name)
            file= open(Name, "r")
            # print("okok")
            con=file.read()
            f=open(Name, "w")
            f.close()
            if(len(con)>0):
                print('New messages:- ',con)
                with open(Name, "rb") as f:
                    ftp.storbinary(f"STOR {Name}", f, blocksize=1024*1024)
                
            else:
                pass
            os.remove(Name)
        # print("done get message")

    def funct_1():
        while(1):
            get_messgae()
            time.sleep(1)
    thread1=threading.Thread(target=funct_1)
    try:
        thread1.start()
        while(1):
            # get_messgae(ftp)
            send_message(ftp)
            # get_messgae(ftp)
    except Exception as e:
        print(e)
        print("[-]Some Error Occured")

    print("[*]Press 1 to exit")
    if(input()=="1"): break



    # #print cwd
    # print(ftp.pwd())
    # #listfiles in cwd
    # print(fnames)



# send QUIT command to the FTP server and close the connection
ftp.quit()
print("Bye!")