from patientRecords.quick_sort import quick_sort
from Users.Doctors import Doctor

class Record:
    def __init__(self, recordID, Date, Time, Doctor, Patient, Symptoms, Diagnosis, Treatment, Medication, results, notes):
        """
        Initialize a patient record.
        :param recordID: Unique identifier for the record.
        :param Date: Date of the record.
        :param Time: Time of the record.
        :param Doctor: Doctor associated with the record.
        :param Patient: Patient associated with the record.
        :param Symptoms: Symptoms reported by the patient.
        :param Diagnosis: Diagnosis made by the doctor.
        :param Treatment: Treatment prescribed.
        :param Medication: Medication prescribed.
        :param results: Test results.
        :param notes: Additional notes.
        """
        self.recordID = recordID
        self.Date = Date
        self.Time = Time
        self.Doctor = Doctor
        self.Patient = Patient
        self.Symptoms = Symptoms
        self.Diagnosis = Diagnosis
        self.Treatment = Treatment
        self.Medication = Medication
        self.results = results
        self.notes = notes

    def get_summary(self):
        """
        Get a summary of the record.
        :return: Dictionary containing the record details.
        """
        return {
            "recordID": self.recordID,
            "Date": self.Date,
            "Time": self.Time,
            "Doctor": self.Doctor,
            "Patient": self.Patient,
            "Symptoms": self.Symptoms,
            "Diagnosis": self.Diagnosis,
            "Treatment": self.Treatment,
            "Medication": self.Medication,
            "results": self.results,
            "notes": self.notes,
        }

class PatientRecordManager:
    def __init__(self):
        """
        Initialize the patient record manager.
        """
        self.records = []  # List to store all patient records
        self.doctors = {}  # Dictionary to store Doctor objects by their ID

    def add_doctor(self, doctor):
        """
        Add a Doctor object to the manager.
        :param doctor: A Doctor object.
        """
        self.doctors[doctor.DoctorID] = doctor

    def add_record(self, record):
        """
        Add a new patient record.
        :param record: A dictionary representing the patient record.
        """
        # Ensure the Doctor field is a Doctor object
        if isinstance(record['Doctor'], int):  # If Doctor is an ID, fetch the Doctor object
            record['Doctor'] = self.doctors.get(record['Doctor'])
        self.records.append(record)

    def update_record(self, recordID, updated_record):
        """
        Update an existing patient record.
        :param recordID: The ID of the record to update.
        :param updated_record: The updated record data.
        :return: True if the update was successful, False otherwise.
        """
        for record in self.records:
            if record['recordID'] == recordID:
                # Ensure the Doctor field is a Doctor object
                if 'Doctor' in updated_record and isinstance(updated_record['Doctor'], int):
                    updated_record['Doctor'] = self.doctors.get(updated_record['Doctor'])
                record.update(updated_record)
                return True
        return False

    def sort_records(self, key=lambda x: x['Date']):
        """
        Sort all patient records using Quick Sort.
        :param key: Key function to sort by (default is 'Date').
        :return: Sorted list of patient records.
        """
        self.records = quick_sort(self.records, key)
        return self.records

    def view_records(self):
        """
        View all patient records.
        :return: A formatted string of all patient records.
        """
        if not self.records:
            return "No patient records available."

        records_summary = []
        for record in self.records:
            records_summary.append(
                f"Record ID: {record['recordID']}, "
                f"Date: {record['Date']}, "
                f"Patient: {record['Patient']}, "
                f"Doctor: {record['Doctor'].Name}"  # Access the Doctor's name
            )
        return "\n".join(records_summary)