import streamlit as st
import sqlite3
import pandas as pd

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
conn = sqlite3.connect("college.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------------------
# CREATE STUDENTS TABLE
# ---------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    year INTEGER
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT
)
""")

conn.commit()

# ---------------------------
# TITLE
# ---------------------------
st.title("🎓 Student ERP System")

# ---------------------------
# SIDEBAR MENU
# ---------------------------
menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Student",
        "View Students",
        "Mark Attendance",
        "Attendance Report"
    ]
)
# ---------------------------
# ADD STUDENT
# ---------------------------
if menu == "Add Student":

    st.header("➕ Add Student")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    name = st.text_input("Student Name")

    department = st.selectbox(
        "Department",
        [
            "Statistics",
            "Computer Science",
            "Mathematics",
            "Physics",
            "Commerce"
        ]
    )

    year = st.selectbox(
        "Year",
        [1, 2, 3]
    )

    if st.button("Add Student"):

        try:
            cursor.execute(
                """
                INSERT INTO students
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    name,
                    department,
                    year
                )
            )
  

            conn.commit()

            st.success("Student Added Successfully ✅")

        except:
            st.error("Student ID Already Exists ❌")

# ---------------------------
# VIEW STUDENTS
# ---------------------------
elif menu == "View Students":

    st.header("📋 Student Records")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM students
        """,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
  
    )
    st.metric(
    "Total Students",
    len(df)
)
elif menu == "Mark Attendance":

    st.header("📝 Mark Attendance")

    students = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if len(students) == 0:

        st.warning(
            "Please add students first."
        )

    else:

        student_id = st.selectbox(
            "Student ID",
            students["student_id"]
        )

        date = st.date_input(
            "Date"
        )

        status = st.selectbox(
            "Status",
            ["Present", "Absent"]
        )

        if st.button(
            "Save Attendance"
        ):

            cursor.execute(
                """
                INSERT INTO attendance
                (student_id, date, status)
                VALUES (?, ?, ?)
                """,
                (
                    student_id,
                    str(date),
                    status
                )
            )

            conn.commit()

            st.success(
                "Attendance Saved ✅"
            )


elif menu == "Attendance Report":

    st.header(
        "📊 Attendance Report"
    )

    df = pd.read_sql_query(
        """
        SELECT *
        FROM attendance
        """,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    if len(df) > 0:

        present = len(
            df[
                df["status"] == "Present"
            ]
        )

        total = len(df)

        percentage = (
            present / total
        ) * 100

        st.metric(
            "Attendance %",
            f"{percentage:.2f}%"
        )