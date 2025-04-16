from medicalHistory.heap_sort import heap_sort
from Users.Patient import patient
from Users.Doctors import Doctor

class history:
    def __init__(self, patient, doctor, age, diagnosis, injuries, medications, allergies):
        """
        Initialize a medical history object.
        :param patient: Patient object associated with the history.
        :param doctor: Doctor object who made the diagnosis.
        :param age: Age of the patient.
        :param diagnosis: List of diagnoses.
        :param injuries: List of injuries.
        :param medications: List of medications.
        :param allergies: List of allergies.
        """
        self.patient = patient  # Patient object
        self.doctor = doctor  # Doctor object
        self.age = age
        self.diagnosis = diagnosis
        self.injuries = injuries
        self.medications = medications
        self.allergies = allergies

    def get_summary(self):
        """
        Get a summary of the patient's medical history.
        :return: Dictionary containing the patient's medical history.
        """
        return {
            "patient_id": self.patient.getPatientID(),
            "patient_name": self.patient.getName(),
            "doctor_name": self.doctor.Name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "injuries": self.injuries,
            "medications": self.medications,
            "allergies": self.allergies,
        }


class MedicalHistoryManager:
    def __init__(self):
        """
        Initialize the medical history manager.
        """
        self.medical_histories = []  # List to store all medical history entries
        self.patients = {}  # Dictionary to store Patient objects by their ID
        self.doctors = {}  # Dictionary to store Doctor objects by their ID

    def add_patient(self, patient_obj):
        """
        Add a Patient object to the manager.
        :param patient_obj: A Patient object.
        """
        self.patients[patient_obj.getPatientID()] = patient_obj

    def add_doctor(self, doctor_obj):
        """
        Add a Doctor object to the manager.
        :param doctor_obj: A Doctor object.
        """
        self.doctors[doctor_obj.DoctorID] = doctor_obj

    def add_history(self, patient_id, doctor_id, age, diagnosis, injuries, medications, allergies):
        """
        Add a new medical history entry.
        :param patient_id: ID of the patient.
        :param doctor_id: ID of the doctor who made the diagnosis.
        :param age: Age of the patient.
        :param diagnosis: List of diagnoses.
        :param injuries: List of injuries.
        :param medications: List of medications.
        :param allergies: List of allergies.
        """
        patient_obj = self.patients.get(patient_id)
        doctor_obj = self.doctors.get(doctor_id)

        if not patient_obj or not doctor_obj:
            raise ValueError("Invalid patient or doctor ID.")

        new_history = history(
            patient=patient_obj,
            doctor=doctor_obj,
            age=age,
            diagnosis=diagnosis,
            injuries=injuries,
            medications=medications,
            allergies=allergies,
        )
        self.medical_histories.append(new_history)

    def update_history(self, patient_id, updated_entry):
        """
        Update an existing medical history entry.
        :param patient_id: The ID of the patient whose history is being updated.
        :param updated_entry: The updated medical history entry.
        :return: True if the update was successful, False otherwise.
        """
        for entry in self.medical_histories:
            if entry.patient.getPatientID() == patient_id:
                if "doctor_id" in updated_entry:
                    doctor_obj = self.doctors.get(updated_entry["doctor_id"])
                    if not doctor_obj:
                        raise ValueError("Invalid doctor ID.")
                    entry.doctor = doctor_obj
                entry.age = updated_entry.get("age", entry.age)
                entry.diagnosis = updated_entry.get("diagnosis", entry.diagnosis)
                entry.injuries = updated_entry.get("injuries", entry.injuries)
                entry.medications = updated_entry.get("medications", entry.medications)
                entry.allergies = updated_entry.get("allergies", entry.allergies)
                return True
        return False

    def sort_histories(self, key=lambda x: x.diagnosis):
        """
        Sort all medical history entries using heap sort.
        :param key: Key function to sort by (default is 'diagnosis').
        :return: Sorted list of medical history entries.
        """
        self.medical_histories = heap_sort(self.medical_histories, key=lambda x: key(x.get_summary()))
        return self.medical_histories

    def view_histories(self):
        """
        View all medical history entries.
        :return: A formatted string of all medical histories.
        """
        if not self.medical_histories:
            return "No medical histories available."

        histories = []
        for entry in self.medical_histories:
            summary = entry.get_summary()
            histories.append(
                f"Patient ID: {summary['patient_id']}, "
                f"Patient Name: {summary['patient_name']}, "
                f"Doctor: {summary['doctor_name']}, "
                f"Diagnosis: {summary['diagnosis']}, "
                f"Medications: {summary['medications']}"
            )
        return "\n".join(histories)

