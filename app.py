import streamlit as st
import sqlite3
import pandas as pd

# -----------------------

# PAGE SETTINGS

# -----------------------

st.set_page_config(
page_title="School Management System",
page_icon="🏫",
layout="wide"
)

# -----------------------

# ADMIN LOGIN

# -----------------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# -----------------------

# DATABASE CONNECTION

# -----------------------

conn = sqlite3.connect("school.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------

# CREATE TABLES

# -----------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
student_id INTEGER,
date TEXT,
status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
student_id INTEGER,
subject TEXT,
marks INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fees(
student_id INTEGER,
status TEXT
)
""")

conn.commit()

# -----------------------

# SESSION STATE

# -----------------------

if "logged_in" not in st.session_state:
st.session_state.logged_in = False
st.session_state.role = ""

# -----------------------

# LOGIN PAGE

# -----------------------

if st.session_state.logged_in == False:

```
st.title("🏫 School Management System")
st.subheader("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    # ADMIN LOGIN
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        st.session_state.logged_in = True
        st.session_state.role = "admin"
        st.success("Admin Login Successful")
        st.rerun()

    else:

        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )

        result = cursor.fetchone()

        if result:
            st.session_state.logged_in = True
            st.session_state.role = result[0]
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Username or Password")
```

# -----------------------

# ADMIN PORTAL

# -----------------------

elif st.session_state.role == "admin":

```
st.title("Admin Dashboard")

menu = st.sidebar.selectbox(
    "Admin Menu",
    [
        "Dashboard",
        "Create Teacher Account",
        "Create Student Account",
        "View Users"
    ]
)

if menu == "Dashboard":

    st.header("System Overview")

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='teacher'")
    teachers = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric("Total Students", students)
    col2.metric("Total Teachers", teachers)

elif menu == "Create Teacher Account":

    st.header("Create Teacher")

    username = st.text_input("Teacher Username")
    password = st.text_input("Teacher Password")

    if st.button("Create Teacher"):

        try:
            cursor.execute(
                "INSERT INTO users(username,password,role) VALUES (?,?,?)",
                (username, password, "teacher")
            )
            conn.commit()
            st.success("Teacher account created")

        except:
            st.error("Username already exists")

elif menu == "Create Student Account":

    st.header("Create Student")

    username = st.text_input("Student Username")
    password = st.text_input("Student Password")

    if st.button("Create Student"):

        try:
            cursor.execute(
                "INSERT INTO users(username,password,role) VALUES (?,?,?)",
                (username, password, "student")
            )
            conn.commit()
            st.success("Student account created")

        except:
            st.error("Username already exists")

elif menu == "View Users":

    st.header("All Users")

    cursor.execute("SELECT username, role FROM users")
    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Username", "Role"])
        st.dataframe(df)
    else:
        st.info("No users found")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()
```

# -----------------------

# TEACHER PORTAL

# -----------------------

elif st.session_state.role == "teacher":

```
st.title("Teacher Portal")

menu = st.sidebar.selectbox(
    "Teacher Menu",
    ["Upload Attendance", "Upload Marks"]
)

if menu == "Upload Attendance":

    st.header("Upload Attendance")

    student_id = st.number_input("Student ID", min_value=1)
    date = st.date_input("Date")
    status = st.selectbox("Status", ["Present", "Absent"])

    if st.button("Submit Attendance"):

        cursor.execute(
            "INSERT INTO attendance VALUES (?,?,?)",
            (student_id, str(date), status)
        )

        conn.commit()
        st.success("Attendance Saved")

elif menu == "Upload Marks":

    st.header("Upload Marks")

    student_id = st.number_input("Student ID", min_value=1)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0)

    if st.button("Submit Marks"):

        cursor.execute(
            "INSERT INTO marks VALUES (?,?,?)",
            (student_id, subject, marks)
        )

        conn.commit()
        st.success("Marks Uploaded")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()
```

# -----------------------

# STUDENT PORTAL

# -----------------------

elif st.session_state.role == "student":

```
st.title("Student Portal")

student_id = st.number_input("Enter Your Student ID", min_value=1)

menu = st.sidebar.selectbox(
    "Student Menu",
    ["View Attendance", "View Marks", "View Fee Status"]
)

if menu == "View Attendance":

    cursor.execute(
        "SELECT date,status FROM attendance WHERE student_id=?",
        (student_id,)
    )

    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Date", "Status"])
        st.dataframe(df)
    else:
        st.info("No attendance found")

elif menu == "View Marks":

    cursor.execute(
        "SELECT subject,marks FROM marks WHERE student_id=?",
        (student_id,)
    )

    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Subject", "Marks"])
        st.dataframe(df)
    else:
        st.info("No marks found")

elif menu == "View Fee Status":

    cursor.execute(
        "SELECT status FROM fees WHERE student_id=?",
        (student_id,)
    )

    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Fee Status"])
        st.dataframe(df)
    else:
        st.info("No fee record found")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()
```
