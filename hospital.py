from database import Database


class HospitalManagementSystem:
    """Contains patient, doctor and appointment database operations."""

    def __init__(self):
        self.db = Database()

    # ---------------- PATIENT CRUD ----------------

    def add_patient(self, patient):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO patients
                (name, age, gender, phone, email, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                patient.name, patient.age, patient.gender,
                patient.phone, patient.email, patient.address
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_patients(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM patients ORDER BY patient_id")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_patient(self, patient_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM patients WHERE patient_id = %s",
                (patient_id,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def update_patient(self, patient_id, patient):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE patients
                SET name=%s, age=%s, gender=%s, phone=%s,
                    email=%s, address=%s
                WHERE patient_id=%s
            """
            cursor.execute(query, (
                patient.name, patient.age, patient.gender,
                patient.phone, patient.email, patient.address,
                patient_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def delete_patient(self, patient_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM patients WHERE patient_id = %s",
                (patient_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    # ---------------- DOCTOR CRUD ----------------

    def add_doctor(self, doctor):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO doctors (name, specialization, phone, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                doctor.name, doctor.specialization,
                doctor.phone, doctor.email
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_doctors(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM doctors ORDER BY doctor_id")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def update_doctor(self, doctor_id, doctor):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE doctors
                SET name=%s, specialization=%s, phone=%s, email=%s
                WHERE doctor_id=%s
            """
            cursor.execute(query, (
                doctor.name, doctor.specialization,
                doctor.phone, doctor.email, doctor_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def delete_doctor(self, doctor_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM doctors WHERE doctor_id = %s",
                (doctor_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    # ---------------- APPOINTMENT OPERATIONS ----------------

    def book_appointment(self, appointment):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO appointments
                (patient_id, doctor_id, appointment_date,
                 appointment_time, reason)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                appointment.patient_id, appointment.doctor_id,
                appointment.appointment_date,
                appointment.appointment_time, appointment.reason
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_appointments(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT a.appointment_id, p.name AS patient_name,
                       d.name AS doctor_name, d.specialization,
                       a.appointment_date, a.appointment_time,
                       a.reason, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                ORDER BY a.appointment_date, a.appointment_time
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def update_appointment_status(self, appointment_id, status):
        allowed = ("Scheduled", "Completed", "Cancelled")
        if status not in allowed:
            raise ValueError("Invalid appointment status.")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE appointments SET status=%s WHERE appointment_id=%s",
                (status, appointment_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()
