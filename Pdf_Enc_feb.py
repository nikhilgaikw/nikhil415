#done by Nikhil Gaikwad


import os
import PyPDF2
from datetime import datetime
from tkinter import filedialog
import tkinter.messagebox
import math
import pandas as pd
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *


class pdfEncryptor:
    
    #This class is created for encryption of PDF files.
    

    def __init__(self, folder):
        self.folder = folder

    def encryption(self):

        """This function is to encrypt all the  PDF files in the folder  """
        files = os.listdir(self.folder)
        global pdf_files
        for pdf_files in files:
            if pdf_files.endswith(".pdf"):
                global output_file_writer_name
                output_file_writer_name = pdf_files.split(".pdf")[0]
                pdf_files_folder = os.path.join(self.folder, pdf_files)
                pdf_in_file = open(pdf_files_folder, "rb")
                inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
                if inputpdf.isEncrypted:
                    print("oops ", pdf_files, "this file is already encrypted")
                    continue
                pages_no = inputpdf.numPages
                output = PyPDF2.PdfFileWriter()
                for i in range(pages_no):
                    inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
                    output.addPage(inputpdf.getPage(i))
                    output.encrypt(output_file_writer_name)
                global current_time
                current_time = datetime.now().replace(microsecond=0)
                new_current_time = datetime.strftime(current_time, "%Y_%B_%d_%H_%M_%S")
                global output_file
                output_file = output_file_writer_name + "_" + new_current_time + ".pdf"
                output_dir = r"C:\Users\Nikhil.Gaikwad\Desktop\python practice"
                if not os.path.isdir(output_dir):
                    os.mkdir(output_dir)
                global output_file_folder
                output_file_folder = os.path.join(output_dir, output_file)
                with open(output_file_folder, "wb") as outputStream:
                    output.write(outputStream)

                file_size = os.path.getsize(output_file_folder)
                global sizeofFile_KB
                sizeofFile_KB = math.ceil(file_size / 1024)
                print(sizeofFile_KB)
                print(output_file)
                print(pdf_files)
               
                usermail = input("enter the mail id of the enduser: ")
                self.send_email(usermail)
                self.create_csv(usermail)
                self.write_to_db(usermail)

    def create_csv(self,usermail):
        """This function is to generate/update csv with encrypted pdf file details"""
        # print("Inside create :",sizeofFile_KB)
        # print("Inside create :", self.sizeofFile_KB)
        path_csv = os.getcwd()
        csv_file = os.path.join(path_csv, "EncryptedPDFs\encryptedfiles.csv")
        Path = os.path.isfile(csv_file)
        if Path == True:
            df = pd.read_csv(csv_file)
            data = pd.DataFrame([[output_file,output_file_writer_name, sizeofFile_KB, current_time,usermail]],
                                columns=['File Name', 'File Password','FileSize(KB)', 'Encryption Time','User Email Id'])
            df = pd.concat([df, data])

        else:
            data = [output_file, output_file_writer_name,sizeofFile_KB, current_time,usermail]
            columns = ['File Name','File Password', 'FileSize(KB)', 'Encryption Time','User Email Id']
            df = pd.DataFrame(data, columns).T
        df.to_csv(csv_file, index=False)

    def connect_to_db(self):
        """ This function is created for connecting to db """
        global cnx
        global mycursor
        cnx = connection.MySQLConnection(user='root', password='Nikhil@415', host='127.0.0.1', database='Nikhil')
        mycursor = cnx.cursor()

    def close_db(self):
        mycursor.close()
        cnx.commit()
        cnx.close()

    def write_to_db(self,usermail):
        """ This function is created for writing data to db """
        # cnx = connection.MySQLConnection(user='dhoni', password='dhoni07', host='127.0.0.1', database='new_sample')
        # mycursor = cnx.cursor()
        query1 = """ CREATE TABLE IF NOT EXISTS encryptedFiles (file_name VARCHAR(200),file_password VARCHAR(200),filSizeKB int,encyrptionTime DATETIME,userMail VARCHAR(50))"""
        mycursor.execute(query1)
        # query2="""INSERT INTO encryptedFiles (file_name,file_password,filSizeKB,encyrptionTime,userMail) VALUES (%s,%s,%s,%s,%s)"""
        query2 = """INSERT INTO encryptedFiles VALUES (%s,%s,%s,%s,%s)"""
        val=[(output_file,output_file_writer_name,sizeofFile_KB, current_time,usermail)]
        mycursor.executemany(query2,val)
        #
        # query2=""" INSERT INTO encryptedFiles (file_name, filSizeKB,encyrptionTime) VALUES (%s,%s, %s)""",(output_file, sizeofFile_KB, current_time)
        # mycursor.execute(query2)
        # cnx.commit()
        # cnx.close()
    def send_email(self,usermail):
        """This function is created for sending email to the user with encrypted pdf as attachment """


        # libraries to be imported
        # import smtplib
        # from email.mime.multipart import MIMEMultipart
        # from email.mime.text import MIMEText
        # from email.mime.base import MIMEBase
        # from email import encoders

        fromaddr = "gaikwadn253@gmail.com"
        toaddr = usermail

        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = fromaddr

        # storing the receivers email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = "PDF Encryption Successful for %s  !!"%pdf_files

        # string to store the body of the mail
        body = "Your PDF file , %s is successfully encrypted !! \npassword : %s \nPlease find the attachment for encrypted PDF "%(pdf_files,output_file_writer_name)

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # open the file to be sent
        filename = output_file
        attachment = open(output_file_folder, "rb")

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

        # # Authentication
        with open("password.txt","r") as file_obj:
            password=file_obj.read()
        # password="xxxxxxx"
        s.login(fromaddr,password)

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()


def main():
    try:
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showinfo("PDF Encryptor", "Please select a directory")
        folder = filedialog.askdirectory()
        # folder=r"C:\Users\Nikhil.Gaikwad\Desktop\python practice"
        pdfencry = pdfEncryptor(folder)
        pdfencry.connect_to_db()
        pdfencry.encryption()
        pdfencry.close_db()
        tkinter.messagebox.showinfo("PDF Encryptor", "Encryption is successful")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            print(err)
        elif err.errno == errorcode.ER_NO_SUCH_TABLE:
            print("No such table exists in database")

        else:
            print(err)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()


