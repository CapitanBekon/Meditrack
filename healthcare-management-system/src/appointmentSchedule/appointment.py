# Add the parent directory to the system path to allow importing modules from it
import sys
import os
import json  # Import JSON module for data storage
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from merge_sort import merge_sort
from Users.Doctors import Doctor  # Import the Doctor class

class appointment:
    def __init__(self, AppointmentID, Patient, Doctor, DateTime):
        """
        Initialize an appointment object.
        :param AppointmentID: Unique identifier for the appointment.
        :param Patient: Patient object associated with the appointment.
        :param Doctor: Doctor object associated with the appointment.
        :param DateTime: Date and time of the appointment.
        """
        self.AppointmentID = AppointmentID
        self.Patient = Patient
        self.Doctor = Doctor
        self.DateTime = DateTime

    def get_appointment_details(self):
        """
        Retrieve the details of the appointment.
        :return: Dictionary containing appointment details.
        """
        return {
            "AppointmentID": self.AppointmentID,
            "Patient": self.Patient.getName(),
            "Doctor": self.Doctor.Name,
            "DateTime": self.DateTime
        }


class appointmentScheduler:
    def __init__(self):
        """
        Initialize the appointment scheduler.
        """
        self.appointments = []  # List to store all scheduled appointments
        self.nextAppointmentID = 1  # Counter to generate unique appointment IDs

    def schedule(self, Date, Hour, Doctor, Patient):
        """
        Schedule a new appointment.
        :param Date: The date for the appointment (YYYY-MM-DD).
        :param Hour: The hour for the appointment (int, 0-23).
        :param Doctor: Doctor object for the appointment.
        :param Patient: Patient object for the appointment.
        :return: True if the appointment was successfully scheduled, False otherwise.
        """
        if Doctor.checkAvailability(Date, Hour):
            Doctor.bookHour(Date, Hour)
            new_appointment = appointment(
                AppointmentID=self.nextAppointmentID,
                Patient=Patient,
                Doctor=Doctor,
                DateTime=f"{Date} {Hour}:00"
            )
            self.appointments.append(new_appointment)
            self.nextAppointmentID += 1
            return True
        return False

    def suggestAvailableSlots(self, Doctor, date):
        """
        Suggest available time slots for a doctor on a specific date.
        :param Doctor: Doctor object to check availability.
        :param date: The date (YYYY-MM-DD) to check for available slots.
        :return: A sorted list of available time slots.
        """
        if date not in Doctor.daysWorking:
            return []  # No working hours on this date
        hours_working, hours_booked = Doctor.daysWorking[date]
        available_slots = [{"time": hour} for hour in hours_working if hour not in hours_booked]
        sorted_slots = merge_sort(available_slots)
        return [slot["time"] for slot in sorted_slots]

    def cancel(self, AppointmentID):
        """
        Cancel an existing appointment.
        :param AppointmentID: The ID of the appointment to cancel.
        :return: True if the appointment was successfully canceled, False otherwise.
        """
        for appointment in self.appointments:
            if appointment.AppointmentID == AppointmentID:
                # Remove the appointment from the list
                self.appointments.remove(appointment)

                # Free up the doctor's booked hour
                date, time = appointment.DateTime.split(" ")
                time = int(time.split(":")[0])  # Extract the hour
                if date in appointment.Doctor.daysWorking and time in appointment.Doctor.daysWorking[date][1]:
                    appointment.Doctor.daysWorking[date][1].remove(time)

                return True  # Appointment successfully canceled
        return False  # Appointment not found

    def reschedule(self, AppointmentID, NewDate, NewTime):
        """
        Reschedule an existing appointment.
        :param AppointmentID: The ID of the appointment to reschedule.
        :param NewDate: The new date for the appointment (YYYY-MM-DD).
        :param NewTime: The new time for the appointment (int).
        :return: True if the appointment was successfully rescheduled, False otherwise.
        """
        for appointment in self.appointments:
            if appointment.AppointmentID == AppointmentID:
                if appointment.Doctor.checkAvailability(NewDate, NewTime):
                    # Free up the old booked hour
                    old_date, old_time = appointment.DateTime.split(" ")
                    old_time = int(old_time.split(":")[0])
                    if old_date in appointment.Doctor.daysWorking and old_time in appointment.Doctor.daysWorking[old_date][1]:
                        appointment.Doctor.daysWorking[old_date][1].remove(old_time)

                    # Book the new hour
                    appointment.Doctor.bookHour(NewDate, NewTime)

                    # Update the appointment details
                    appointment.DateTime = f"{NewDate} {NewTime}:00"

                    return True
        return False

    def viewAppointments(self):
        """
        View all scheduled appointments.
        :return: A formatted string of all appointments.
        """
        if not self.appointments:
            return "No appointments scheduled."
        
        schedule = []
        for appointment in self.appointments:
            details = appointment.get_appointment_details()
            schedule.append(
                f"AppointmentID: {details['AppointmentID']}, "
                f"Patient: {details['Patient']}, "
                f"Doctor: {details['Doctor']}, "
                f"DateTime: {details['DateTime']}"
            )
        return "\n".join(schedule)

    def save_to_json(self, filename):
        """
        Save all appointments to a JSON file.
        :param filename: The name of the JSON file.
        """
        data = [
            {
                "AppointmentID": appointment.AppointmentID,
                "Patient": appointment.Patient.getName(),
                "Doctor": appointment.Doctor.Name,
                "DateTime": appointment.DateTime
            }
            for appointment in self.appointments
        ]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename):
        """
        Load all appointments from a JSON file.
        :param filename: The name of the JSON file.
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.appointments = []
            for appointment_data in data:
                new_appointment = appointment(
                    AppointmentID=appointment_data["AppointmentID"],
                    Patient=appointment_data["Patient"],  # Replace with actual Patient object
                    Doctor=appointment_data["Doctor"],  # Replace with actual Doctor object
                    DateTime=appointment_data["DateTime"]
                )
                self.appointments.append(new_appointment)

            if self.appointments:
                self.nextAppointmentID = max(a.AppointmentID for a in self.appointments) + 1
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with empty data.")


# Example usage of the appointmentScheduler
scheduler = appointmentScheduler()

# Load appointments from JSON
scheduler.load_from_json("appointments.json")

# Save appointments to JSON
scheduler.save_to_json("appointments.json")