import pandas as pd
import plotly.express as px
import streamlit as st
import sqlite3

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
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    mark INTEGER
)
""")

conn.commit()

# ---------------------------
# TITLE
# ---------------------------
st.title("🎓 Student ERP Portal")

# ---------------------------
# SIDEBAR MENU
# ---------------------------
menu = st.sidebar.selectbox(
    "Select Option",
[
    "Dashboard",
    "Add Student",
    "View Students",
    "Mark Attendance",
    "Attendance Report",
    "Add Marks",
    "View Marks",
    "Student Report",
    "Upload Students",
    "Delete Student"
]
)
# ---------------------------
# ADD STUDENT
# ---------------------------
if menu == "Dashboard":

    st.header("📊 Dashboard")

    students_df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    attendance_df = pd.read_sql_query(
        "SELECT * FROM attendance",
        conn
    )

    marks_df = pd.read_sql_query(
        "SELECT * FROM marks",
        conn
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            len(students_df)
        )

    with col2:
        st.metric(
            "📝 Attendance Records",
            len(attendance_df)
        )

    with col3:

        avg_mark = 0

        if len(marks_df) > 0:
            avg_mark = round(
                marks_df["mark"].mean(),
                2
            )

        st.metric(
            "📚 Average Marks",
            avg_mark
        )
    if len(marks_df) > 0:

            st.subheader("📊 Academic Performance Analysis")

            fig = px.bar(
                marks_df,
                x="subject",
                y="mark",
                title="Subject Wise Marks"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
# ---------------------------
# PERFORMANCE INSIGHTS
# ---------------------------
            
            best_subject = marks_df.loc[
                marks_df["mark"].idxmax()
            ]

            weak_subject = marks_df.loc[
                 marks_df["mark"].idxmin()
            ]

            st.success(
                f"🏆 Best Subject: {best_subject['subject']} ({best_subject['mark']})"
            )

            st.warning(
                f"⚠️ Needs Improvement: {weak_subject['subject']} ({weak_subject['mark']})"
            )

            st.info(
                f"📈 Performance Gap: {best_subject['mark'] - weak_subject['mark']} Marks"
            )

            ranking_df = marks_df.sort_values(
                 by="mark",
                ascending=False
            )

            ranking_df = ranking_df[
                ["subject", "mark"]
            ]

            ranking_df.index = range(
                1,
                len(ranking_df) + 1
            )
            ranking_df.index.name = "Rank"

            st.subheader("🏅 Subject Rankings")

            st.dataframe(
                ranking_df,
                use_container_width=True
            )
        
            highest_mark = marks_df["mark"].max()
            lowest_mark = marks_df["mark"].min()

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🏆 Highest Mark",
                    highest_mark
             )

            with col2:
                st.metric(
                     "📉 Lowest Mark",
                    lowest_mark
            )   
elif menu == "Add Student":

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
            "Food Chemistry",
            "Visual communication",
            "Digital Journalism",
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
        
elif menu == "Add Marks":

    st.header("📚 Add Marks")

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

        subject = st.text_input(
            "Subject"
        )

        mark = st.number_input(
            "Mark",
            min_value=0,
            max_value=100
        )

        if st.button(
            "Save Marks"
        ):

            cursor.execute(
                """
                INSERT INTO marks
                (student_id, subject, mark)
                VALUES (?, ?, ?)
                """,
                (
                    student_id,
                    subject,
                    mark
                )
            )

            conn.commit()

            st.success(
                "Marks Saved Successfully ✅"
            )
        
        
        
elif menu == "View Marks":

        

            st.header(
        "📋 Student Marks"
    )

            df = pd.read_sql_query(
        """
        SELECT *
        FROM marks
        """,
        conn
    )

            st.dataframe(df)

            if len(df) > 0:

                st.metric(
            "Average Mark",
            round(
                df["mark"].mean(),
                2
            )
        )
            
elif menu == "Student Report":

    st.header("📑 Student Report")

    students_df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if len(students_df) == 0:

        st.warning("No students found")

    else:

        student_id = st.selectbox(
            "Select Student",
            students_df["student_id"]
        )

        student_info = students_df[
            students_df["student_id"] == student_id
        ]

        st.subheader("🎓 Student Information")

        st.write(
            "Name:",
            student_info["name"].values[0]
        )

        st.write(
            "Department:",
            student_info["department"].values[0]
        )

        st.write(
            "Year:",
            student_info["year"].values[0]
        )

        marks_df = pd.read_sql_query(
            f"""
            SELECT *
            FROM marks
            WHERE student_id = {student_id}
            """,
            conn
        )

        attendance_df = pd.read_sql_query(
            f"""
            SELECT *
            FROM attendance
            WHERE student_id = {student_id}
            """,
            conn
        )

        st.subheader("📚 Academic Performance")

        if len(marks_df) > 0:

            avg_mark = round(
                marks_df["mark"].mean(),
                2
            )

            st.metric(
                "Average Mark",
                avg_mark
            )

            report_marks = marks_df[
                ["subject", "mark"]
            ]

            st.dataframe(
                report_marks,
                use_container_width=True
            )

        if len(attendance_df) > 0:

            present = len(
                attendance_df[
                    attendance_df["status"] == "Present"
                ]
            )

            attendance_percentage = round(
                (present / len(attendance_df)) * 100,
                2
            )

            st.metric(
                "Attendance %",
                attendance_percentage
            )

elif menu == "Upload Students":

    st.header("📤 Upload Students")

    uploaded_file = st.file_uploader(
        "Choose Excel File",
        type=["xlsx"]
    )

    if uploaded_file is not None:

        df = pd.read_excel(
            uploaded_file
        )
        df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df.columns
        ]

        st.subheader("Preview")

        st.dataframe(df)

        if st.button(
                "Import Students"
        ):

                for _, row in df.iterrows():

                    try:

                        cursor.execute(
                            """
                            INSERT INTO students
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                row["student_id"],
                                row["name"],
                                row["department"],
                                row["year"]
                            )
                )

                    except:
                        pass

        conn.commit()

        st.success(
            "Students Imported Successfully ✅"
        )
        st.metric(
            "Imported Students",
            len(df)
        )
elif menu == "Delete Student":

    st.header("🗑️ Delete Student")

    students_df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if len(students_df) == 0:

        st.warning(
            "No Students Found"
        )

    else:

        student_id = st.selectbox(
            "Select Student ID",
            students_df["student_id"]
        )

        if st.button(
            "Delete Student"
        ):

            cursor.execute(
                """
                DELETE FROM students
                WHERE student_id = ?
                """,
                (student_id,)
            )

            conn.commit()

            st.success(
                "Student Deleted Successfully ✅"
            )        