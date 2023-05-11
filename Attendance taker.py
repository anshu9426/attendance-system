import time
import getpass
import warnings
from tqdm.auto import tqdm
import sqlite3
import pyzbar.pyzbar as pyzbar
import pyqrcode
import cv2
import os
import numpy
import colorama
from colorama import Back, Style
warnings.filterwarnings("ignore")
colorama.init(autoreset=True)
#------ScanningFromWebCamera---------------------
def scan():
	i = 0
	cap = cv2.VideoCapture(0)
	font = cv2.FONT_HERSHEY_PLAIN
	while i<1:
		ret,frame=cap.read()
		decode = pyzbar.decode(frame)
		for obj in decode:
			name=obj.data
			name2= name.decode()
			ii = name2.split(' ')
			db = sqlite3.connect('StudentDatabase.db')
			c = db.cursor()
			c.execute('''CREATE TABLE IF NOT EXISTS Record(iid TEXT, TimeofMArk TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
			c.execute("INSERT INTO Record( iid) VALUES (?)", (ii))
			c.execute("SELECT student_name,student_room from all_record where student_id=(?)", (ii))
			rows = c.fetchall()
			print("                                                                       ")
			print("                                                                       ")
			print("-----------------------------------------------------------------------")
			for row in rows:
				print(row)
			print("Has marked his attendence .")
			print("-----------------------------------------------------------------------")
			print("                                                                       ")
			db.commit()
			warnings.filterwarnings("ignore")

#database portions--------------------------------
			i=i+1
		cv2.imshow("QRCode",frame)
		cv2.waitKey(2)
		cv2.destroyAllWindows
	warnings.filterwarnings("ignore")
	scan()

#------CreateDatabaseForeEmployee------------------
def database():
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS all_record(student_name TEXT, student_id TEXT, student_contact, student_room TEXT)")
	conn.commit()
	conn.close()
database()

#------AddingNewUsers/Employee---------------------
def add_User():
	Li = []
	S_name=str(input("Please Enter Student Name\n"))
	S_id=str(input("Please Enter Student Enrollment No\n"))
	S_contac= input("Please enter Student Contact No\n")
	S_room= input("Please enter Student Room No\n")
	Li.extend((S_name,S_id,S_contac,S_room))
#-----using List Compression to convert a list to str--------------
	listToStr = ' '.join([str(elem) for elem in Li])
	#print(listToStr)
	print(Back.YELLOW + "Please Verify the Information")
	print("Student Name       = "+ S_name)
	print("Student ID         = "+ S_id)
	print("Student Contact    = "+ S_contac)
	print("Student Room = "+ S_room)
	input("Press Enter to continue or CTRL+C to Break Operation")
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("INSERT INTO all_record(student_name, student_id, student_contact, student_room) VALUES (?,?,?,?)", (S_name,S_id,S_contac,S_room))
	conn.commit()
	conn.close()
	print("+------------------------------+")
	markattendance()

#--------------ViewDatabase------------------------
def viewdata():
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	# c.execute('''CREATE TABLE IF NOT EXISTS Record(iid TEXT, TimeofMArk TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
	c.execute("SELECT * FROM all_record")
	rows = c.fetchall()
	for row in rows:
		print(row)
	conn.close()
	print("+------------------------------+")
	markattendance()
#----------AdminScreen-----------------------
def afterlogin():
	print("+------------------------------+")
	print("|  1- Add New Student          |")
	print("|  2- Veiw Record              |")
	print("|  3- Main Menu                |")
	print("+------------------------------+")
	user_input = input("")
	if user_input == '1':
		add_User()
	if user_input == '2':
		viewdata()
	if user_input == '3':
		markattendance()

#Login--------------------------------------
def login():
	c=0
	print(Back.CYAN+ 'Please Enter Password :')
	print(Back.YELLOW+"     IHA           ")
	password = getpass.getpass()
	if(password==0):
		markattendance()
	if password =='KASHI':
		for i in tqdm(range(4000)):
			print("",end='\r')
		print("------------------------------------------------------------------------------------------------------------------------")
		print(Back.BLUE+"     IHA           ")
		afterlogin()
	if password != 'Kaashi':
		print("Invalid Password")
		login()
	



#-------MainPage----------------------------
def markattendance():
	print("+------------------------------+")
	print("|  1- Mark Attendance          |")
	print("|  2- Admin Login              |")
	print("|  3- Exit                     |")
	print("+------------------------------+")
	user_input2 = input("")
	if user_input2== '1':
		scan()
	if user_input2 == '2':
		login()
	if user_input2 == '3':
		exit()
markattendance()