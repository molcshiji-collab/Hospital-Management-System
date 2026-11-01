
import streamlit as st
import pandas as pd

from hospital import HospitalManagementSystem
from models import Patient, Doctor, Appointment

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

hms = HospitalManagementSystem()

st.title("🏥 Hospital Management System")
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a page",
    [
        "Dashboard",
        "Patients",
        "Doctors",
        "Appointments"
    ]
)

# DASHBOARD
if page == "Dashboard":
    st.subheader("Hospital Dashboard")

    patients = hms.get_patients()
    doctors = hms.get_doctors()
    appointments = hms.get_appointments()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", len(patients))
    col2.metric("Total Doctors", len(doctors))
    col3.metric("Total Appointments", len(appointments))

    st.subheader("Recent Appointments")

    if appointments:
        st.dataframe(pd.DataFrame(appointments), use_container_width=True)
    else:
        st.info("No appointments available.")

# PATIENTS
elif page == "Patients":
    st.subheader("Patient Management")

    with st.form("patient_form"):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_area("Address")

        submitted = st.form_submit_button("Add Patient")

        if submitted:
            if name.strip() and phone.strip():
                patient = Patient(
                    name, age, gender, phone, email, address
                )
                try:
                    patient_id = hms.add_patient(patient)
                    st.success(f"Patient added! ID: {patient_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter patient name and phone.")

    st.subheader("All Patients")

    patients = hms.get_patients()

    if patients:
        st.dataframe(pd.DataFrame(patients), use_container_width=True)
    else:
        st.info("No patients found.")

# DOCTORS
elif page == "Doctors":
    st.subheader("Doctor Management")

    with st.form("doctor_form"):
        name = st.text_input("Doctor Name")
        specialization = st.text_input("Specialization")
        phone = st.text_input("Phone")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Doctor")

        if submitted:
            if name.strip() and specialization.strip() and phone.strip():
                doctor = Doctor(name, specialization, phone, email)
                try:
                    doctor_id = hms.add_doctor(doctor)
                    st.success(f"Doctor added! ID: {doctor_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter name, specialization and phone.")

    st.subheader("All Doctors")

    doctors = hms.get_doctors()

    if doctors:
        st.dataframe(pd.DataFrame(doctors), use_container_width=True)
    else:
        st.info("No doctors found.")

# APPOINTMENTS
elif page == "Appointments":
    st.subheader("Appointment Management")

    patients = hms.get_patients()
    doctors = hms.get_doctors()

    if not patients or not doctors:
        st.warning("Add at least one patient and one doctor first.")
    else:
        patient_options = {
            f"{p['name']} (ID: {p['patient_id']})": p['patient_id']
            for p in patients
        }

        doctor_options = {
            f"{d['name']} (ID: {d['doctor_id']})": d['doctor_id']
            for d in doctors
        }

        with st.form("appointment_form"):
            patient_label = st.selectbox(
                "Select Patient", list(patient_options.keys())
            )
            doctor_label = st.selectbox(
                "Select Doctor", list(doctor_options.keys())
            )
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")
            reason = st.text_area("Reason")

            submitted = st.form_submit_button("Book Appointment")

            if submitted:
                appointment = Appointment(
                    patient_options[patient_label],
                    doctor_options[doctor_label],
                    appointment_date,
                    appointment_time,
                    reason
                )

                try:
                    appointment_id = hms.book_appointment(appointment)
                    st.success(
                        f"Appointment booked! ID: {appointment_id}"
                    )
                except Exception as e:
                    st.error(f"Booking failed: {e}")

    st.subheader("All Appointments")

    appointments = hms.get_appointments()

    if appointments:
        st.dataframe(pd.DataFrame(appointments), use_container_width=True)

        appointment_ids = [
            a["appointment_id"] for a in appointments
        ]

        selected_id = st.selectbox(
            "Select Appointment ID to update",
            appointment_ids
        )

        new_status = st.selectbox(
            "New Status",
            ["Scheduled", "Completed", "Cancelled"]
        )

        if st.button("Update Appointment Status"):
            try:
                updated = hms.update_appointment_status(
                    selected_id, new_status
                )
                if updated:
                    st.success("Appointment status updated!")
                    st.rerun()
                else:
                    st.warning("No appointment was updated.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("No appointments found.")
