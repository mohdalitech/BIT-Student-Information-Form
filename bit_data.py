import streamlit as st
import mysql.connector
import json
connection = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    port=int(st.secrets["mysql"]["port"]),
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)
cursor=connection.cursor()
st.set_page_config(
    page_title="Student Information Form",
    layout="wide"
)
admin_page = st.Page("pages/admin.py",title="Admin Page")
pg=st.navigation([admin_page],position="hidden")

col1,col2=st.columns(2)
with col1:
    st.header("🎓STUDENT INFORMATION FORM")
with col2:
    if(st.button("Admin Page",type="primary")):
        st.switch_page(admin_page)
st.divider()
student_id=st.text_input("Enter your student id :",placeholder="BIT_001",width=500)
Student_Name=st.text_input("Enter your name :",placeholder="Rajit",width=500)
Gender=st.selectbox(
    "Choose your gender :",
    ["M","F"],
    width=500
)
cgpa=st.number_input("Enter your current cgpa : ",placeholder="8.12",width=500)
Attendance_Percentage=st.number_input("What is percentage of your attendance ?",placeholder="75.5",width=500)
Total_distance=st.number_input("Enter total distance from home to BIT ?",placeholder="20.00",width=500)
Roll_No=st.text_input("Enter your 13 digit roll no :",placeholder="1234567890012",width=500)
Address=st.text_area("What is the your address ?",placeholder="Complete address",width=500)
dob=st.date_input("Enter your date of birth : ",width=500)
Class_Time=st.time_input("At what time class starts ? ",width=500)
Admission_DateTime=st.datetime_input("When have you taken admission ? ",width=500)
Skills=st.text_input("Enter your 3 skills comma separated : ",placeholder="python,java,writing",width=500)
Semester_Status=st.selectbox(
    "What is your semester status ? ",
    ["Active","Completed","Dropped"],
    width=500
)
if "view_response" not in st.session_state:
    st.session_state.view_response=False
if st.button("Submit Your Response",type="primary"):
    skills=[skill.strip() for skill in Skills.split(",")]
    if(len(skills)!=3):
        st.toast("Skills count is not 3!")
    sql="""SELECT Student_ID FROM btech_3rd_year
            WHERE Student_ID=%s
        """
    cursor.execute(sql,(student_id,))
    result=cursor.fetchone()
    if result:
        st.error("A record with this student_id already exists!")
    else:
        sql="""
        INSERT INTO btech_3rd_year
        (Student_ID,Student_Name,Gender,cgpa,Attendance_Percentage,Total_distance,Roll_No,Address,dob,Class_Time,Admission_DateTime,Skills,Semester_Status)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql,(student_id,Student_Name,Gender,cgpa,Attendance_Percentage,Total_distance,Roll_No,Address,dob,Class_Time,Admission_DateTime,json.dumps(skills),Semester_Status))
        connection.commit()
        st.success("Your response has been recorded..!")
        st.session_state.view_response=True
    if(st.session_state.view_response):
        try:
            cursor=connection.cursor(dictionary=True)
            sql="""
            SELECT * FROM btech_3rd_year
            WHERE Student_ID=%s
            """
            cursor.execute(sql,(student_id,))
            records=cursor.fetchall()
            if records:
                st.dataframe(records,use_container_width=True)
            else:
                st.error("No records found!!")
        except Exception as e:
            st.error(f"Error fetching record:{e}")
pg.run()
