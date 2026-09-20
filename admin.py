import streamlit as st
import mysql.connector
connections=mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)
cursor=connections.cursor()
st.header("🛡️ ADMIN PAGE- STUDENT INFORMATION FORM")
st.divider()
if "admin_verified" not in st.session_state:
    st.session_state.admin_verified=False
admin_name=st.text_input("Enter the admin username : ")
admin_pass=st.text_input("Enter the admin password : ")
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
            connections.commit()
        else:
            st.success("The data has not been erased!!")
else:
    st.error("Try entering correct credentials if you're are valid admin!")