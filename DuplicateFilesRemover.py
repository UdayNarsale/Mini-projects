
from sys import *
import os
import hashlib
import time
import smtplib
from email.message import EmailMessage
import time
import datetime
import schedule

def task():
    print("Mail sent......")
    print("Current time is : ", datetime.datetime.now())
    SendAutomationMail(argv[1])

def hashfile(path,bolcksize=1024):
    afile=open(path,'rb')
    hasher=hashlib.md5()
    buf=afile.read(bolcksize)
    while len(buf)>0:
        hasher.update(buf)
        buf=afile.read(bolcksize)
    afile.close()
    return hasher.hexdigest()

def SendAutomationMail(path):
    print("Current time is : ",datetime.datetime.now())
    msg=EmailMessage()
    msg['Subject']='Email by using Automation'
    msg['From']='automation7517@gmail.com'
    msg['To']='automation4783@gmail.com'
    msg.set_content('is image Email is sent or NOT?')
    DirectoryDusplicateRemoval(path)

    for dirName,subdirs,fileList in os.walk(path):
        for file in fileList:
            path=os.path.join(dirName,file)
            with open(file,'rb') as f:
                file_data=f.read()
                file_name=f.name
            msg.add_attachment(file_data,maintype='asd',subtype='files',filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login("automation7517@gmail.com","chetan123")
        server.send_message(msg)


def DirectoryDusplicateRemoval(path):
    flag=os.path.isabs(path)
    if flag==False:
        path=os.path.abspath(path)
    exists=os.path.isdir(path)
    unique=dict()
    if exists:
        os.chdir(path)
        fd=open('logdelete.txt','w')
        for dirName,subdirs,fileList in os.walk(path):
            print("Current folder is :"+dirName)
            for filen in fileList:
                path=os.path.join(dirName,filen)
                file_hash=hashfile(path)
                if file_hash not in unique:
                    unique[file_hash]=filen

                else:

                    fd.write(filen+'\n')
                    os.remove(filen)

                #print(' ')
    else:
        print("Invalid Path")

def main():
    start=time.time()
    print("---- Marvellous Infosystems by Chetan Khemnar ----")

    print("Application name : " +argv[0])
    #print(argv[1],argv[2],argv[3])
    if (len(argv) != 2):
        print("Error : Invalid number of arguments")
        exit()
    
    if (argv[1] == "-h") or (argv[1] == "-H"):
        print("This Script accepts 1 arguments from command line")
        exit()

    if (argv[1] == "-u") or (argv[1] == "-U"):
        print("usage : ApplicationName AbsolutePath_of_Directory")
        exit()

    try:
        print("Schedular starts.....")
        schedule.every(1).minutes.do(task)
        end=time.time()
        print("Execution time",end-start)
      
    except ValueError:
        print("Error : Invalid datatype of input")

    except Exception:
        print("Error : Invalid input")

    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == "__main__":
    main()
