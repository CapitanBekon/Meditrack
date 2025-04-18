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

    def schedule(self, ProposedDate, ProposedTime, Doctor, Patient):
        """
        Schedule a new appointment.
        :param ProposedDate: The proposed date for the appointment.
        :param ProposedTime: The proposed time for the appointment.
        :param Doctor: Doctor object for the appointment.
        :param Patient: Patient object for the appointment.
        :return: True if the appointment was successfully scheduled, False otherwise.
        """
        # Check if the doctor is available at the proposed date and time
        if Doctor.checkAvailability(ProposedDate, ProposedTime):
            # Book the hour for the doctor
            Doctor.bookHour(ProposedDate, ProposedTime)

            # Create a new appointment object
            new_appointment = appointment(
                AppointmentID=self.nextAppointmentID,
                Patient=Patient,
                Doctor=Doctor,
                DateTime=f"{ProposedDate} {ProposedTime}:00"
            )

            # Add the appointment to the list of scheduled appointments
            self.appointments.append(new_appointment)

            # Increment the appointment ID counter
            self.nextAppointmentID += 1

            return True  # Appointment successfully scheduled
        return False  # Doctor is not available at the proposed time

    def suggestAvailableSlots(self, Doctor, day):
        """
        Suggest available time slots for a doctor on a specific day.
        :param Doctor: Doctor object to check availability.
        :param day: The day to check for available slots.
        :return: A sorted list of available time slots.
        """
        if day not in Doctor.daysWorking:
            return []  # No working hours on this day

        hours_working, hours_booked = Doctor.daysWorking[day]

        # Find available hours by excluding booked hours
        available_slots = [{"time": hour} for hour in hours_working if hour not in hours_booked]

        # Sort the available slots using merge_sort
        sorted_slots = merge_sort(available_slots)

        # Return the sorted list of available slots
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
                appointment.Doctor.daysWorking[date][1].remove(time)

                return True  # Appointment successfully canceled
        return False  # Appointment not found

    def reschedule(self, AppointmentID, NewDate, NewTime):
        """
        Reschedule an existing appointment.
        :param AppointmentID: The ID of the appointment to reschedule.
        :param NewDate: The new date for the appointment.
        :param NewTime: The new time for the appointment.
        :return: True if the appointment was successfully rescheduled, False otherwise.
        """
        for appointment in self.appointments:
            if appointment.AppointmentID == AppointmentID:
                # Check if the doctor is available at the new date and time
                if appointment.Doctor.checkAvailability(NewDate, NewTime):
                    # Free up the old booked hour
                    old_date, old_time = appointment.DateTime.split(" ")
                    old_time = int(old_time.split(":")[0])  # Extract the hour
                    appointment.Doctor.daysWorking[old_date][1].remove(old_time)

                    # Book the new hour for the doctor
                    appointment.Doctor.bookHour(NewDate, NewTime)

                    # Update the appointment details
                    appointment.DateTime = f"{NewDate} {NewTime}:00"

                    return True  # Appointment successfully rescheduled
        return False  # Appointment not found or doctor not available

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
                # Create appointment objects from JSON data
                new_appointment = appointment(
                    AppointmentID=appointment_data["AppointmentID"],
                    Patient=appointment_data["Patient"],  # Replace with actual Patient object
                    Doctor=appointment_data["Doctor"],  # Replace with actual Doctor object
                    DateTime=appointment_data["DateTime"]
                )
                self.appointments.append(new_appointment)

            # Update the nextAppointmentID
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