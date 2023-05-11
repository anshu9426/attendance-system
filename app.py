import cv2
import getpass
import os
import sqlite3
import pyzbar.pyzbar as pyzbar
import pyqrcode
import streamlit as st
from tqdm.auto import tqdm
import warnings

# Initialize the database
def initialize_database():
    print("khmala")
    conn = sqlite3.connect('StudentDatabase.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS all_record(student_name TEXT, student_id TEXT, student_contact, student_room)")
    c.execute('''CREATE TABLE IF NOT EXISTS Record(iid TEXT, TimeofMark TIMESTAMP DEFAULT (datetime('now', 'localtime')) NOT NULL)''')
    conn.commit()
    conn.close()
initialize_database()
# Add a new user/employee to the database
def add_user():
    print("zwla")
    print('add user called')
    Li = []
    S_name = st.text_input("Please Enter Student Name")
    S_id = st.text_input("Please Enter Student Id")
    S_contac = st.text_input("Please enter Student Contact No")
    S_room = st.text_input("Please enter Student Room No")
    # S_subject = st.text_input("Please Enter Subject Name\n")
    
    Li.extend((S_name, S_id, S_contac, S_room))
    if st.button("Add User"):
        # Using list comprehension to convert a list to string
        listToStr = ' '.join([str(elem) for elem in Li])
        st.write("Please Verify the Information")
        st.write("Student Name       = ", S_name)
        st.write("Student ID         = ", S_id)
        st.write("Student Contact    = ", S_contac)
        st.write("Student Room       = ", S_room)
        # st.write("Subject Name       = ", S_subject)
        print(S_contac)
       
        conn = sqlite3.connect('StudentDatabase.db')
        c = conn.cursor()
        c.execute("INSERT INTO all_record(student_name, student_id, student_contact, student_room) VALUES (?,?,?,?)", (S_name,S_id,S_contac,S_room))
        conn.commit()
        conn.close()
        st.success("User added successfully")
        mark_attendance()
    print('add user success')        

# View the database records
def view_database():
    print("dla")
    conn = sqlite3.connect('StudentDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM all_record")
    rows = c.fetchall()
    st.write(rows)
    conn.close()
    if st.button("Back to menu"):
        mark_attendance()
# View marked attendance
def view_marked_attendance():
    print("mla")
    conn = sqlite3.connect('StudentDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Record")
    rows = c.fetchall()
    st.write(rows)
    conn.close()
    if st.button("Back to menu"):
        mark_attendance()
# Admin login
def login():
    password = st.text_input("Please Enter Password", type="password")
    if password == "":
        mark_attendance()
    elif password == 'KASHI':
        for i in tqdm(range(4000)):
            pass
        st.write("Admin Login successful")
        after_login()
    elif password != 'Kaashi':
        st.error("Invalid Password")
        login()

# After successful login, display the admin options
def after_login():
    print("zwla")
    st.write("+------------------------------+")
    st.write("|  1- Add New Student          |")
    st.write("|  2- View Record              |")
    st.write("|  3- View Marked Attendance   |")
    st.write("|  4- Main Menu                |")
    st.write("+------------------------------+")
    user_input = st.selectbox("Please select an option", ["1", "2", "3","4"], key='key')
    if user_input == '1':
        add_user()
    if user_input == '2':
        view_database()
    if user_input == '3':
        view_marked_attendance()
    if user_input == '4':
        mark_attendance()

# Scan QR code using the webcam
def scan():
    print("kwla")
    i = 0
    cap = cv2.VideoCapture(0)
    # font = cv2.FONT_HERSHEY_PLAIN-----ME-1
    while i<1:
        ret, frame = cap.read()
        decode = pyzbar.decode(frame)

        # print(decode , type(decode)  , len(decode) )    

        if( len(decode) != 0 ):
        # ME-2
            for obj in decode:
                name = obj.data
                name2 = name.decode()
                ii = name2.split(' ')
                db = sqlite3.connect('StudentDatabase.db')
                c = db.cursor()
                # c.execute('''CREATE TABLE IF NOT EXISTS Record(iid TEXT, TimeofMark TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')
                c.execute('''CREATE TABLE IF NOT EXISTS Record(iid TEXT, TimeofMark TIMESTAMP DEFAULT (datetime('now', 'localtime')) NOT NULL)''')
                c.execute("INSERT INTO Record(iid) VALUES (?)", (ii))
                c.execute("SELECT student_name, student_room FROM all_record WHERE student_id=(?)", (ii))
                rows = c.fetchall()

                st.write("-------------------------")
                for row in rows:
                    st.write(row)
                st.write("Has marked their attendance.")
                st.write("-------------------------")
                db.commit()
                warnings.filterwarnings("ignore")
                i = i + 1
        # ------------------M3
        cv2.imshow("QRCode", frame)
        cv2.waitKey(2)
        cv2.destroyAllWindows
    warnings.filterwarnings("ignore")
    # scan()

# Mark Attendance
def mark_attendance():
    print('howla')
    st.write("+------------------------------+")
    st.write("|        MARK ATTENDANCE       |")
    st.write("+------------------------------+")
    st.write("| 1. Scan QR Code              |")
    st.write("| 2. Admin login               |")
    st.write("| 3. Exit                      |")
    st.write("+------------------------------+")
    choice = st.selectbox("Please select an option:", ["Scan QR Code", "Admin login", "Exit"], key='view')
    if choice == "Scan QR Code":
        scan()
    elif choice == "Admin login":
        login()
    elif choice == "Exit":
        exit()
mark_attendance()