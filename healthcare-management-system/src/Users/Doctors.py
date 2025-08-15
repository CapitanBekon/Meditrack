import json
from datetime import date, timedelta, datetime

class Doctor:
    def __init__(self, DoctorID, Name, daysWorking):
        """
        Initialize a Doctor object.
        :param DoctorID: Unique identifier for the doctor.
        :param Name: Name of the doctor.
        :param daysWorking: Dictionary with keys as dates (YYYY-MM-DD) and values as 2D arrays 
                            [[hours_working], [hours_booked]].
        """
        self.DoctorID = DoctorID
        self.Name = Name
        self.daysWorking = daysWorking 

    def getDaysWorking(self):
        """
        Get the dates the doctor is working along with their hours.
        :return: Dictionary of dates and their corresponding hours.
        """
        return self.daysWorking

    def setDaysWorking(self, daysWorking):
        """
        Set the dates the doctor is working along with their hours.
        :param daysWorking: Dictionary with keys as dates (YYYY-MM-DD) and values as 2D arrays [[hours_working], [hours_booked]].
        """
        self.daysWorking = daysWorking

    def checkAvailability(self, date, hour):
        """
        Check if the doctor is available at a specific date and hour.
        :param date: The date to check (YYYY-MM-DD).
        :param hour: The hour to check (e.g., 10).
        :return: True if available, False otherwise.
        """
        if date in self.daysWorking:
            hours_working, hours_booked = self.daysWorking[date]
            if hour in hours_working and hour not in hours_booked:
                return True
        return False

    def bookHour(self, date, hour):
        """
        Book an hour for the doctor on a specific date.
        :param date: The date to book (YYYY-MM-DD).
        :param hour: The hour to book (e.g., 10).
        :return: True if booking was successful, False otherwise.
        """
        if self.checkAvailability(date, hour):
            self.daysWorking[date][1].append(hour)  # Add hour to hours_booked
            return True
        return False

    def viewSchedule(self):
        """
        View the doctor's schedule.
        :return: A formatted string showing the schedule.
        """
        schedule = []
        for date_key, hours in self.daysWorking.items():
            hours_working, hours_booked = hours
            schedule.append(f"{date_key}: Working Hours: {hours_working}, Booked Hours: {hours_booked}")
        return "\n".join(schedule)

    def updateProfile(self, Name, Specialization):
        """
        Update the doctor's profile.
        :param Name: New name for the doctor.
        :param Specialization: New specialization for the doctor.
        """
        self.Name = Name
        self.Specialization = Specialization

    def save_to_json(self, filename):
        """
        Save the doctor's data to a JSON file.
        :param filename: The name of the JSON file.
        """
        data = {
            "DoctorID": self.DoctorID,
            "Name": self.Name,
            "daysWorking": self.daysWorking
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        """
        Load the doctor's data from a JSON file.
        :param filename: The name of the JSON file.
        :return: A Doctor object.
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            return cls(
                DoctorID=data["DoctorID"],
                Name=data["Name"],
                daysWorking=data.get("daysWorking", {})
            )
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None

    def migrate_legacy_day_keys(self, reference_day: date | None = None):
        """
        Convert legacy weekday-name keys (e.g., 'Monday') in daysWorking to concrete YYYY-MM-DD date keys.
        If reference_day is not provided, today is used to compute the next occurrence of that weekday.
        When merging into an existing date key, working/booked hours are deduplicated and booked hours are
        kept only if also present in working hours.
        """
        if not self.daysWorking:
            return

        ref = reference_day or date.today()
        # Map weekday names to Python weekday indices (Mon=0..Sun=6)
        weekday_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        def is_iso_date(s: str) -> bool:
            try:
                datetime.strptime(s, "%Y-%m-%d")
                return True
            except Exception:
                return False

        legacy_keys = [k for k in list(self.daysWorking.keys()) if not is_iso_date(k)]
        for key in legacy_keys:
            idx = weekday_map.get(str(key).strip().lower())
            if idx is None:
                # Unknown legacy key; drop it safely
                self.daysWorking.pop(key, None)
                continue
            days_ahead = (idx - ref.weekday()) % 7
            target = ref + timedelta(days=days_ahead)
            date_key = target.strftime("%Y-%m-%d")

            src_work, src_booked = self.daysWorking.get(key, [[], []])
            dst_work, dst_booked = self.daysWorking.get(date_key, [[], []])

            # Merge and dedupe
            merged_work = sorted(set(dst_work) | set(src_work))
            merged_booked = sorted((set(dst_booked) | set(src_booked)) & set(merged_work))

            self.daysWorking[date_key] = [merged_work, merged_booked]
            # Remove legacy key
            self.daysWorking.pop(key, None)