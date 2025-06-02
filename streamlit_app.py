import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from config import API_URL

def dashboard():
    st.title("Employee Dashboard")
    try:
        data = requests.get(API_URL).json()
        df = pd.DataFrame(data)
        st.dataframe(df)

        if not df.empty:
            st.metric("Average Salary", f"${df['salary'].mean():.2f}")
            st.bar_chart(df['department'].value_counts())
            st.hist(df['salary'], bins=10)
            st.pyplot(plt)
    except:
        st.error("Could not load data")

def manage():
    st.title("Manage Employees")

    with st.form("add_form"):
        st.subheader("Add Employee")
        name = st.text_input("Name")
        dept = st.text_input("Department")
        salary = st.number_input("Salary")
        date = st.date_input("Hire Date")
        if st.form_submit_button("Add"):
            requests.post(API_URL, json={
                "name": name, "department": dept,
                "salary": salary, "hire_date": str(date)
            })
            st.success("Added successfully")
            st.experimental_rerun()

    emp_id = st.number_input("Employee ID", step=1)
    if st.button("Delete"):
        requests.delete(f"{API_URL}/{emp_id}")
        st.success("Deleted")
        st.experimental_rerun()

    with st.form("update_form"):
        st.subheader("Update Employee")
        name = st.text_input("New Name")
        dept = st.text_input("New Department")
        salary = st.number_input("New Salary")
        date = st.date_input("New Hire Date")
        if st.form_submit_button("Update"):
            requests.put(f"{API_URL}/{emp_id}", json={
                "name": name, "department": dept,
                "salary": salary, "hire_date": str(date)
            })
            st.success("Updated")
            st.experimental_rerun()

page = st.sidebar.radio("Pages", ["Dashboard", "Manage Employees"])
if page == "Dashboard":
    dashboard()
else:
    manage()
