import mysql.connector
from hospital import HospitalManagementSystem
from models import Patient, Doctor, Appointment


def show_rows(rows):
    if not rows:
        print("No records found.")
        return
    for row in rows:
        print("-" * 55)
        for key, value in row.items():
            print(f"{key}: {value}")
    print("-" * 55)


def read_patient():
    name = input("Patient name: ").strip()
    age = int(input("Age: "))
    gender = input("Gender: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email (optional): ").strip()
    address = input("Address (optional): ").strip()

    if not name or age <= 0 or not gender or not phone:
        raise ValueError("Name, positive age, gender and phone are required.")

    return Patient(name, age, gender, phone, email, address)


def read_doctor():
    name = input("Doctor name: ").strip()
    specialization = input("Specialization: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email (optional): ").strip()

    if not name or not specialization or not phone:
        raise ValueError("Name, specialization and phone are required.")

    return Doctor(name, specialization, phone, email)


def main():
    hms = HospitalManagementSystem()

    while True:
        print("\\n========== HOSPITAL MANAGEMENT SYSTEM ==========")
        print("1. Add patient")
        print("2. View all patients")
        print("3. Search patient by ID")
        print("4. Update patient")
        print("5. Delete patient")
        print("6. Add doctor")
        print("7. View doctors")
        print("8. Update doctor")
        print("9. Delete doctor")
        print("10. Book appointment")
        print("11. View appointments")
        print("12. Update appointment status")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                patient = read_patient()
                new_id = hms.add_patient(patient)
                print(f"Patient added. Patient ID: {new_id}")

            elif choice == "2":
                show_rows(hms.get_patients())

            elif choice == "3":
                patient_id = int(input("Enter patient ID: "))
                patient = hms.get_patient(patient_id)
                show_rows([patient] if patient else [])

            elif choice == "4":
                patient_id = int(input("Patient ID to update: "))
                if not hms.get_patient(patient_id):
                    print("Patient ID not found.")
                else:
                    patient = read_patient()
                    if hms.update_patient(patient_id, patient):
                        print("Patient updated successfully.")
                    else:
                        print("No changes made.")

            elif choice == "5":
                patient_id = int(input("Patient ID to delete: "))
                confirm = input("Confirm delete? (y/n): ").lower()
                if confirm == "y":
                    print("Patient deleted." if hms.delete_patient(patient_id)
                          else "Patient ID not found.")

            elif choice == "6":
                doctor = read_doctor()
                new_id = hms.add_doctor(doctor)
                print(f"Doctor added. Doctor ID: {new_id}")

            elif choice == "7":
                show_rows(hms.get_doctors())

            elif choice == "8":
                doctor_id = int(input("Doctor ID to update: "))
                doctor = read_doctor()
                print("Doctor updated." if hms.update_doctor(doctor_id, doctor)
                      else "Doctor ID not found.")

            elif choice == "9":
                doctor_id = int(input("Doctor ID to delete: "))
                confirm = input("Confirm delete? (y/n): ").lower()
                if confirm == "y":
                    print("Doctor deleted." if hms.delete_doctor(doctor_id)
                          else "Doctor ID not found.")

            elif choice == "10":
                patient_id = int(input("Patient ID: "))
                doctor_id = int(input("Doctor ID: "))
                date = input("Appointment date (YYYY-MM-DD): ").strip()
                time = input("Appointment time (HH:MM:SS): ").strip()
                reason = input("Reason for visit: ").strip()

                appointment = Appointment(
                    patient_id, doctor_id, date, time, reason
                )
                new_id = hms.book_appointment(appointment)
                print(f"Appointment booked. Appointment ID: {new_id}")

            elif choice == "11":
                show_rows(hms.get_appointments())

            elif choice == "12":
                appointment_id = int(input("Appointment ID: "))
                print("1. Scheduled  2. Completed  3. Cancelled")
                status_choice = input("Choose status: ").strip()
                statuses = {
                    "1": "Scheduled",
                    "2": "Completed",
                    "3": "Cancelled"
                }
                if status_choice not in statuses:
                    print("Invalid status choice.")
                else:
                    updated = hms.update_appointment_status(
                        appointment_id, statuses[status_choice]
                    )
                    print("Status updated." if updated else "Appointment not found.")

            elif choice == "0":
                print("Thank you for using Hospital Management System.")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as error:
            print(f"Input error: {error}")
        except mysql.connector.Error as error:
            print(f"MySQL error: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
