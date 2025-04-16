import Patient
import User
from appointmentSchedule.appointment import appointment
from patientRecords.record import Record
from medicalHistory.history import history

class Doctor:
    def __init__(self, DoctorID, Name, daysWorking):
        """
        Initialize a Doctor object.
        :param DoctorID: Unique identifier for the doctor.
        :param Name: Name of the doctor.
        :param daysWorking: Dictionary with keys as days (e.g., 'Monday') and values as 2D arrays 
                            [[hours_working], [hours_booked]].
        """
        self.DoctorID = DoctorID
        self.Name = Name
        self.daysWorking = daysWorking  # Example: {'Monday': [[9, 10, 11], [9, 10]]}

    def getDaysWorking(self):
        """
        Get the days the doctor is working along with their hours.
        :return: Dictionary of days and their corresponding hours.
        """
        return self.daysWorking

    def setDaysWorking(self, daysWorking):
        """
        Set the days the doctor is working along with their hours.
        :param daysWorking: Dictionary with keys as days and values as 2D arrays [[hours_working], [hours_booked]].
        """
        self.daysWorking = daysWorking #append fix

    def checkAvailability(self, day, hour):
        """
        Check if the doctor is available at a specific day and hour.
        :param day: The day to check (e.g., 'Monday').
        :param hour: The hour to check (e.g., 10).
        :return: True if available, False otherwise.
        """
        if day in self.daysWorking:
            hours_working, hours_booked = self.daysWorking[day]
            if hour in hours_working and hour not in hours_booked:
                return True
        return False

    def bookHour(self, day, hour):
        """
        Book an hour for the doctor on a specific day.
        :param day: The day to book (e.g., 'Monday').
        :param hour: The hour to book (e.g., 10).
        :return: True if booking was successful, False otherwise.
        """
        if self.checkAvailability(day, hour):
            self.daysWorking[day][1].append(hour)  # Add hour to hours_booked
            return True
        return False

    def viewSchedule(self):
        """
        View the doctor's schedule.
        :return: A formatted string showing the schedule.
        """
        schedule = []
        for day, hours in self.daysWorking.items():
            hours_working, hours_booked = hours
            schedule.append(f"{day}: Working Hours: {hours_working}, Booked Hours: {hours_booked}")
        return "\n".join(schedule)

    def updateProfile(self, Name, Specialization):
        """
        Update the doctor's profile.
        :param Name: New name for the doctor.
        :param Specialization: New specialization for the doctor.
        """
        self.Name = Name
        self.Specialization = Specialization