from re import sub
import smtplib
smtp_object = smtplib.SMTP('smtp.gmail.com',587)
smtp_object.ehlo()
smtp_object.starttls()
import getpass
email = getpass.getpass("enter your mail: ")
password = getpass.getpass("enter your password: ")
smtp_object.login(email,password)

#now sending mail
from_adderss = getpass.getpass("enter your mail: ")
to_address = getpass.getpass("enter mail of your recipents: ")
subject = input("enter a subject line: ")
message = input("enter a message you want: ")
msg = "Subject: " + subject + '\n' + message
smtp_object.sendmail(from_adderss,to_address)

smtp_object.quit()

