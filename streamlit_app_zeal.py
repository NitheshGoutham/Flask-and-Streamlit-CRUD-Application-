import streamlit as st
import pandas as pd
import requests
import time
import warnings
from streamlit_option_menu import option_menu

warnings.filterwarnings("ignore")

API_URL = "http://127.0.0.1:5000"  

with st.sidebar:
    selected = option_menu("Main Menu",
                           options=["CREATE", "READ", "UPDATE", "DELETE"],
                           default_index=1,
                           orientation="vertical")


def fetch_records():
    response = requests.get(f"{API_URL}/records")
    if response.status_code == 200:
        records = response.json()
        return pd.DataFrame(records, columns=["id", "name", "email", "phone_number", "role", "experience", "current_ctc", "expected_ctc", "notice_period"])
    else:
        st.error("Error fetching records.")
        return pd.DataFrame(columns=["id", "name", "email", "phone_number", "role", "experience", "current_ctc", "expected_ctc", "notice_period"])

def record_exists(email, phone_number, exclude_id=None):
    records_df = fetch_records()
    if not records_df.empty:
        if exclude_id is not None:
            records_df = records_df[records_df["id"] != exclude_id]
        return ((records_df["email"] == email) | (records_df["phone_number"] == phone_number)).any()
    return False

def add_record(name, email, phone_number, role, experience, current_ctc, expected_ctc, notice_period):
    data = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "role": role,
        "experience": experience,
        "current_ctc": current_ctc,
        "expected_ctc": expected_ctc,
        "notice_period": notice_period
    }
    response = requests.post(f"{API_URL}/record", json=data)
    return response.status_code == 201

def update_record(record_id, name, email, phone_number, role, experience, current_ctc, expected_ctc, notice_period):
    data = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "role": role,
        "experience": experience,
        "current_ctc": current_ctc,
        "expected_ctc": expected_ctc,
        "notice_period": notice_period
    }
    response = requests.put(f"{API_URL}/record/{record_id}", json=data)
    return response.status_code == 200

def delete_record(record_id):
    response = requests.delete(f"{API_URL}/record/{record_id}")
    return response.status_code == 200

role_options = ["Software Engineer", "Associate Software Engineer", "Fullstack Developer"]

notice_period_options = ["Immediate Joiner", "Less than 15 days", "1 month", "2 months", "3 months"]

if selected == "CREATE":
    st.title("Add a New Record")
    with st.form("add_record_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        role = st.selectbox("Role", role_options)
        experience = st.number_input("Experience (years)", min_value=0, step=1)
        current_ctc = st.number_input("Current CTC (lakhs)", min_value=0.0, step=0.1)
        expected_ctc = st.number_input("Expected CTC (lakhs)", min_value=0.0, step=0.1)
        notice_period = st.selectbox("Notice Period", notice_period_options)
        submitted = st.form_submit_button("Add Record")

        if submitted and name and email and phone_number:
            if record_exists(email, phone_number):
                st.error("The provided details already exist in the database.")
            else:
                if add_record(name, email, phone_number, role, experience, current_ctc, expected_ctc, notice_period):
                    st.success("Record added successfully!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Failed to add record.")

elif selected == "READ":
    st.title("Existing Records")
    records_df = fetch_records()
    if not records_df.empty:
        st.dataframe(records_df)
    else:
        st.write("No records found.")

elif selected == "UPDATE":
    st.title("Update Records")
    records_df = fetch_records()
    if not records_df.empty:
        for index, row in records_df.iterrows():
            record_id = row["id"]
            with st.expander(f"Update Record {record_id}"):
                new_name = st.text_input("Name", row["name"], key=f"name_{record_id}")
                new_email = st.text_input("Email", row["email"], key=f"email_{record_id}")
                new_phone_number = st.text_input("Phone Number", row["phone_number"], key=f"phone_{record_id}")
                new_role = st.selectbox("Role", role_options, index=role_options.index(row["role"]) if row["role"] in role_options else 0, key=f"role_{record_id}")
                new_experience = st.number_input("Experience", value=row["experience"], min_value=0.0, step=0.1, key=f"experience_{record_id}")
                new_current_ctc = st.number_input("Current CTC", value=row["current_ctc"], min_value=0.0, step=0.1, key=f"current_ctc_{record_id}")
                new_expected_ctc = st.number_input("Expected CTC", value=row["expected_ctc"], min_value=0.0, step=0.1, key=f"expected_ctc_{record_id}")
                new_notice_period = st.selectbox("Notice Period", notice_period_options, index=notice_period_options.index(row["notice_period"]) if row["notice_period"] in notice_period_options else 0, key=f"notice_{record_id}")

                if st.button("Update", key=f"update_{record_id}"):
                    if record_exists(new_email, new_phone_number, exclude_id=record_id):
                        st.error("The provided email or phone number already exists in another record.")
                    else:
                        if update_record(record_id, new_name, new_email, new_phone_number, new_role, new_experience, new_current_ctc, new_expected_ctc, new_notice_period):
                            st.success(f"Record {record_id} updated successfully!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"Failed to update record {record_id}.")
                        

elif selected == "DELETE":
    st.title("Delete Records")
    records_df = fetch_records()
    if not records_df.empty:
        for index, row in records_df.iterrows():
            record_id = row["id"]
            with st.expander(f"Delete Record {record_id}"):
                st.write(f"Name: {row['name']}")
                st.write(f"Email: {row['email']}")
                st.write(f"Phone Number: {row['phone_number']}")
                
                if st.button("Delete", key=f"delete_{record_id}"):
                    if delete_record(record_id):
                        st.success(f"Record {record_id} deleted successfully!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"Failed to delete record {record_id}.")
    else:
        st.write("No records to delete.")
