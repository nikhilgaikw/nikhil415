# import PyPDF2
# import tkinter
# from tkinter import filedialog
# from datetime import datetime
# ##file_name = open("one.pdf",'rb')
# ##root = tkinter.Tk()
# ##root.withdraw()
# #file_name = filedialog.askopenfilename()

# #pdf_folder = r"C:\Users\91897\Desktop\Corporate_Trainings\BBI\PDF_File_Encryption"

# pdf_in_file = open('one.pdf','rb')

# inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
# pages_no = inputpdf.numPages
# output = PyPDF2.PdfFileWriter()

# for i in range(pages_no):
#     inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
    
#     output.addPage(inputpdf.getPage(i))
#     output.encrypt('admin@123')
#     current_time = datetime.now()
#     #with open("simple_password_protected.pdf", "wb") as outputStream:
#     with open(current_time, "wb") as outputStream:
#         output.write(outputStream)

# pdf_in_file.close()

import mysql.connector
import userdetails
import logging
import tkinter
from tkinter import filedialog
import csv
import smtplib


""""Program to send the mail based on the operation..."""
class Demo:
    logging.basicConfig(filename="database.log",level=logging.DEBUG)

    def __init__(self, database):
        self.database = database
        # self.table_name = table_name

    def create_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to be created : ")
            id = input("Enter first column name : ")
            id_type = input("Data type : ")
            f_name = input("Enter second column name : ")
            f_name_type = input("Data type : ")
            l_name = input("Enter third column name : ")
            l_name_type = input("Data type : ")
            address = input("Enter fourth column name : ")
            address_type = input("Data type : ")
            # (ID Integer, F_NAME text, L_NAME text, ADDRESS text)
            query = f'CREATE TABLE {t_name} ({id} {id_type},{f_name} {f_name_type}, {l_name} {l_name_type} , {address} {address_type})'
            my_cursor.execute(query)
            db_connection.commit()
            self.send_mail()
            print("CREATED")
            logging.debug("Suscessfully table created")

        except Exception as e:
            print(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def insert_data_to_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name in which you want to insert data : ")
            print("Please insert these details to add it to the table :  ")
            id = input("Enter the id of student : ")
            f_name = input("Enter the first name of student : ")
            l_name = input("Enter the last name of student : ")
            add = input("Enter the address of student : ")
            query = f'INSERT INTO {t_name} values(%s, %s, %s, %s)'
            val = (id, f_name, l_name, add)
            my_cursor.execute(query,val)
            db_connection.commit()
            self.send_mail()
            print("Inserted")
            logging.debug("Successfully inserted data")

        except Exception as e:
            print(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()



    def delete_from_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database='mydatabase')
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to delete the data : ")
            id = int(input('Enter the ID of the student which u want to delete : '))
            query = f'DELETE FROM {t_name} WHERE ID={id}'
            my_cursor.execute(query)
            db_connection.commit()
            self.send_mail()
            print("Deleted...")
            logging.debug( "Successfully deleted from table")

        except Exception as e:
            print(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def update_table_data(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to update table data : ")
            print("Enter details to Update table data : ")
            id = int(input("Enter the student proper Id : "))
            val = input("Enter the value which you want to update : ")
            column_name = input("Enter the column name whose data you want to update : ")

            query = f'UPDATE {t_name} set {column_name} = "{val}" WHERE ID={id}'
            my_cursor.execute(query)
            db_connection.commit()
            self.send_mail()
            print("UPDATED...")
            logging.warning('Successfully updated data into table')

        except Exception as e:
            print(e)
            logging.warning(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def drop_a_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name drop : ")
            query = f'DROP TABLE {t_name}'
            my_cursor.execute(query)
            db_connection.commit()
            self.send_mail()
            print("Table dropped....")
            logging.debug( "Successfully dropped table")

        except Exception as e:
            print(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def show_data_from_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to view data : ")
            query = f'SELECT * FROM {t_name}'
            my_cursor.execute(query)
            data = my_cursor.fetchall()

            for datas in data:
                print(datas)
            db_connection.commit()
            self.send_mail()
            print("Displaying....")
            logging.debug("Successfully fetched all data")

        except Exception as e:
            print(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()

    def show_tables(self):
        db_connetion = None

        try:
            db_connetion = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=userdetails.database_name)
            my_cursor = db_connetion.cursor()
            my_cursor.execute("""SHOW TABLES""")
            data = my_cursor.fetchall()
            for i in range(len(data)):
                print(i + 1, ". ", data[i][0])
            db_connetion.commit()
            return data

        except Exception as e:
            print(e)

        finally:
            if db_connetion != None:
                db_connetion.close()

    def read_data_from_csv(self):
        root = tkinter.Tk()
        root.withdraw()
        try:
            file = filedialog.askopenfilename()
            l_email = []
            with open(file, 'r') as file_obj:
                csv_obj = csv.reader(file_obj)
                header = next(csv_obj)

                for i in csv_obj:
                    l_email.append(i)
            return l_email

        except Exception as e:
            print(e)

    def send_mail(self):
        mail = None

        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login(userdetails.s_email, userdetails.s_password)
            lst = self.read_data_from_csv()
            for i in range(len(lst)):
                # print(i, lst[i])
                if lst[i][1] == 'create':
                    # print(lst[i][0])
                    msg = "Table has been created Created"
                    mail.sendmail(userdetails.s_email, lst[i][0], msg)
                elif lst[i][1] == 'update':
                    # print(lst[i][0])
                    msg = "Table has been Updated"
                    mail.sendmail(userdetails.s_email, lst[i][0], msg)
                elif lst[i][1] == 'insert':
                    # print(lst[i][0])
                    msg = "Data has been Inserted into table"
                    mail.sendmail(userdetails.s_email, lst[i][0], msg)
                elif lst[i][1] == "delete":
                    msg = "Particular row has been Deleted"
                    mail.sendmail(userdetails.s_email, lst[i][0], msg)
                elif lst[i][1] == 'drop':
                    msg = "Table Dropped"
                    mail.sendmail(userdetails.s_email, lst[i][0], msg)
                elif lst[i][1] == 'showdata':
                    msg = "Showed Data from database table"
                    mail.sendmail(userdetails.s_email, lst[i][0], msg)
                else:
                   print("No such operation found")
            print("Email sent Successfully ")

        except Exception as e:
            print(e)
        finally:
            if mail != None:
                mail.quit()


database = input("Enter your databse name : ")

while True:
    d = Demo(database)
    user_choice = int(input('''Enter your choice :
1.CREATE TABLE
2.INSERT DATA
3.DELETE FROM TABLE
4.UPDATE TABLE DATA
5.DROP A TABLE
6.SHOW DATA
7.SHOW ALL TABLES\n'''))

    if user_choice == 1:
        d.create_table()
    elif user_choice == 2:
        d.insert_data_to_table()
    elif user_choice == 3:
        d.delete_from_table()
    elif user_choice == 4:
        d.update_table_data()
    elif user_choice == 5:
        d.drop_a_table()
    elif user_choice == 6:
        d.show_data_from_table()
    elif user_choice == 7:
        d.show_tables()
    else:
        print("INVALID INPUT......")

    choice = input("Do you want to continue (y/n) : ")
    if choice == 'y' or  choice == 'Y':
        continue
    else:
         break