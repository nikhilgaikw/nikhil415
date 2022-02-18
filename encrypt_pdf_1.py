
import os
import PyPDF2
from datetime import datetime
import math



class pdfEncryptor:
    """
    .......This class is created for encryption of PDF files.........
    """
    def __init__(self, folder):
        self.folder = folder

    def encryption(self):

        """ .....This function is to encrypt all the  PDF files in the folder ....... """
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
                    print("Sorry", pdf_files, "is already encrypted")
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
                # global usermail
                usermail = input("enter the mail id of the enduser: ")
                self.send_email(usermail)
                self.create_csv(usermail)
                self.write_to_db(usermail)