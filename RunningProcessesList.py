
import os 
import time
import psutil
from urllib.request import urlopen
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urlopen('https://www.google.co.in/',timeout=1)
        return True
    except:
        return False

def MailSender(filename,time):
    try:
        fromaddrs=argv[3]
        toaddrs=argv[5]

        msg=MIMEMultipart()

        msg['From']=fromaddrs
        msg['To']=toaddrs

        body="""
        Hello %s,
        Welcome to Marvellous Infosystems.
        please find attached document which contains Log of Running process.
        Log file is created at : %s

        This is auto generated mail.

        Thanks & Regards,
        Chetan Shivaji Khemnar
        Marvellous Infosystems
        """%(toaddrs,time)

        Subject="""
        Marvellous Infosystems process log file generated at : %s
        """%(time)
        msg['Subject']=Subject

        msg.attach(MIMEText(body,'plain'))

        attachment=open(filename,'rb')

        p=MIMEBase('application','octet-stream')

        p.set_payload((attachment).read())
        encoders.encode_base64(p)

        p.add_header('Content-Disposition',"attachment; filename=%s"%filename)

        msg.attach(p)

        s=smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddrs,argv[4])

        text=msg.as_string()

        s.sendmail(fromaddrs,toaddrs,text)

        s.quit()
        print("Log file successfully sent through Mail")

    except Exception as E:
        print(E)


def Task():
    ProcInfoLog(argv[2])

def ProcInfoLog(log_dir):
    listprocess=[]
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator='-'*80
    current_time=time.strftime("%Y%m%d-%H%M%S")
    log_path=os.path.join(log_dir,"MarvellousLog%s.log"%(current_time))
    fd=open(log_path,"w")
    fd.write(separator+"\n")
    fd.write("Marvelllous Infosystems Process Logger :"+time.ctime()+"\n")
    fd.write(separator+'\n')

    for proc in psutil.process_iter():
        try:
            pinfo=proc.as_dict(attrs=['pid','name','username'])
            vms=proc.memory_info().vms/(1024*1024)
            pinfo['vms']=vms
            listprocess.append(pinfo)
        except(psutil.NosuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

    for element in listprocess:
        fd.write("%s\n"%element)

    print("Log file is successfully generated at location :",log_path)

    connected=is_connected()

    if connected:
        startTime=time.time()
        MailSender(log_path,time.ctime())
        endTime=time.time()

        print("Took %s seconds to mail"%(endTime-startTime))
    else:
        print("There is no internet connection")

def main():
    print("----Process Automation using Python----")

    print("Application name : ",argv[0])

    if(len(argv)!=6):
        print("Error : Invalid number of arguments")
        exit()
    if(argv[1]=='-h') or(argv[1]=='-H'):
        print("This script is used create log file in that directory which contains information of running processes")
        exit()
    if(argv[1]=='-u') or(argv[1]=='-U'):
        print("Usage : ApplicationName time Directory_Name user_mail_id user_mail_id_password reciever_mail_id")
        exit()
    try:
        print("schedular starts....")
        schedule.every(int(argv[1])).minutes.do(Task)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("Error : Invalid datatype of input")
    except Exception:
        print("Error : Invalid input")  

if __name__=="__main__":
    main()
