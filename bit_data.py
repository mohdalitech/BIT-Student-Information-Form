import streamlit as st
import mysql.connector
import json
@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )
connection=get_db_connection()
cursor=connection.cursor()
col1,col2=st.columns(2)
with col1:
    st.header("🎓STUDENT INFORMATION FORM")
with col2:
    if(st.button("Admin Portal",type="primary")):
        if "admin_verified" not in st.session_state:
            st.session_state.admin_verified=False
    admin_name=st.text_input("Enter the admin username : ")
    admin_pass=st.text_input("Enter the admin password : ")
    if(st.button("Submit",type="primary")):
        if(admin_name==st.secrets["admin_username"] and admin_pass==st.secrets["admin_password"]):
            st.success("Your admin details are verified successfully...!!")
            st.session_state.admin_verified=True
        if(st.session_state.admin_verified):
            st.subheader("All students records:")
            sql="""
            SELECT * FROM btech_3rd_year;
            """
            cursor.execute(sql)
            results=cursor.fetchall()
            if results:
                st.dataframe(results,use_container_width=True)
            else:
                st.error("Not enough records found!")
            if(st.button("Clear All Records",type="primary")):
                confirm_check=st.selectbox(
                    "Do you want to clear record? This action cannot be undone!",
                    ["Yes","No"]
                )
                if(confirm_check=="Yes"):
                    sql="""
                    TRUNCATE TABLE btech_3rd_year
                    """
                    cursor.execute(sql)
                    connection.commit()
                else:
                    st.success("The data has not been erased!!")
        else:
            st.error("Try entering correct credentials if you're are valid admin!")
st.divider()
student_id=st.text_input("Enter your student id :",placeholder="BIT_001")
Student_Name=st.text_input("Enter your name :",placeholder="Rajit")
Gender=st.selectbox(
    "Choose your gender :",
    ["M","F"]
)
cgpa=st.number_input("Enter your current cgpa : ",placeholder="8.12")
Attendance_Percentage=st.number_input("What is percentage of your attendance ?",placeholder="75.5")
Total_distance=st.number_input("Enter total distance from home to BIT ?",placeholder="20.00")
Roll_No=st.text_input("Enter your 13 digit roll no :",placeholder="1234567890012")
Address=st.text_area("What is the your address ?",placeholder="Complete address")
dob=st.date_input("Enter your date of birth : ")
Class_Time=st.time_input("At what time class starts ? ")
Admission_DateTime=st.datetime_input("When have you taken admission ? ")
Skills=st.text_input("Enter your 3 skills comma separated : ",placeholder="python,java,writing")
Semester_Status=st.selectbox(
    "What is your semester status ? ",
    ["Active","Completed","Dropped"]
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
