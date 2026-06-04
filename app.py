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
        "View Students"
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