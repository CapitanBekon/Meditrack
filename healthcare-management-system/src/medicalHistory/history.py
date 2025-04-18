import sys
import os
import json  # Import JSON module for data storage
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heap_sort import heap_sort
from Users.Doctors import Doctor  # Import the Doctor class
from Users.Patient import patient  # Import the Patient class

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
            print(f"Patient ID: {patient_id}, Doctor ID: {doctor_id}")
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

    def save_to_json(self, filename):
        """
        Save all data (patients, doctors, and medical histories) to a JSON file.
        :param filename: The name of the JSON file.
        """
        data = {
            "patients": {pid: vars(patient) for pid, patient in self.patients.items()},
            "doctors": {did: vars(doctor) for did, doctor in self.doctors.items()},
            "medical_histories": [
                {
                    "patient_id": history.patient.getPatientID(),
                    "doctor_id": history.doctor.DoctorID,
                    "age": history.age,
                    "diagnosis": history.diagnosis,
                    "injuries": history.injuries,
                    "medications": history.medications,
                    "allergies": history.allergies,
                }
                for history in self.medical_histories
            ],
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename):
        """
        Load all data (patients, doctors, and medical histories) from a JSON file.
        :param filename: The name of the JSON file.
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            # Load patients
            for pid, patient_data in data["patients"].items():
                self.patients[pid] = patient(**patient_data)

            # Load doctors
            for did, doctor_data in data["doctors"].items():
                self.doctors[did] = Doctor(**doctor_data)

            # Load medical histories
            for history_data in data["medical_histories"]:
                patient_obj = self.patients.get(history_data["patient_id"])
                doctor_obj = self.doctors.get(history_data["doctor_id"])
                if patient_obj and doctor_obj:
                    new_history = history(
                        patient=patient_obj,
                        doctor=doctor_obj,
                        age=history_data["age"],
                        diagnosis=history_data["diagnosis"],
                        injuries=history_data["injuries"],
                        medications=history_data["medications"],
                        allergies=history_data["allergies"],
                    )
                    self.medical_histories.append(new_history)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with empty data.")

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


# Example usage of the MedicalHistoryManager
manager = MedicalHistoryManager()

# Load data from JSON
manager.load_from_json("medical_data.json")

# Add medical history entries
manager.add_history(
    patient_id=1,
    doctor_id=1,
    age=30,
    diagnosis=["Flu"],
    injuries=[],
    medications=["Paracetamol"],
    allergies=["Penicillin"]
)

manager.add_history(
    patient_id=2,
    doctor_id=2,
    age=25,
    diagnosis=["Fracture"],
    injuries=["Arm fracture"],
    medications=["Ibuprofen"],
    allergies=[]
)

# Save data to JSON
manager.save_to_json("medical_data.json")

# View unsorted histories
print("Unsorted Histories:")
print(manager.view_histories())

