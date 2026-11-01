class Patient:
    def __init__(self, name, age, gender, phone, email="", address=""):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address


class Doctor:
    def __init__(self, name, specialization, phone, email=""):
        self.name = name
        self.specialization = specialization
        self.phone = phone
        self.email = email


class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date,
                 appointment_time, reason=""):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
