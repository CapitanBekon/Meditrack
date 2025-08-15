import sys
import os

# Ensure the src directory is on sys.path before any local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Users.User import User, Roles  # Import the User class and Roles for login and permissions

# Predefined users for the login system (for demonstration purposes)
users = {
    "admin": User(user_id="1", username="admin", password="admin123", permission_level=Roles.ADMIN, accountCreated=0),
    "doctor": User(user_id="2", username="doctor", password="doctor123", permission_level=Roles.DOCTOR, accountCreated=0),
    "patient": User(user_id="3", username="patient", password="patient123", permission_level=Roles.PATIENT, accountCreated=0),
}

def main():
    print("Welcome to the Healthcare Management System")
    
    # Login process
    current_user = login()
    if not current_user:
        print("Exiting the system. Goodbye!")
        return

    print(f"\nWelcome, {current_user.username}!")
    
    while True:
        print("\nSelect an option:")
        print("1. Manage Patient Records")
        print("2. Manage Medical History")
        print("3. Schedule Appointments")
        print("4. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Only doctors and admins can manage patient records
            if not current_user.has_permission(Roles.DOCTOR):
                print("Access denied. Requires doctor or admin.")
            else:
                manage_patient_records()
        elif choice == '2':
            # Only doctors and admins can manage medical histories
            if not current_user.has_permission(Roles.DOCTOR):
                print("Access denied. Requires doctor or admin.")
            else:
                manage_medical_history()
        elif choice == '3':
            schedule_appointments(current_user)
        elif choice == '4':
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    """
    Handle user login.
    :return: The logged-in User object or None if login fails.
    """
    print("\nLogin to the Healthcare Management System")
    for _ in range(3):  # Allow up to 3 login attempts
        username = input("Username: ")
        password = input("Password: ")
        
        user = users.get(username)
        if not user:
            print("Invalid username or password. Please try again.")
            continue
        if user.login(username, password):
            return user
    
    print("Too many failed login attempts.")
    return None

def manage_patient_records():
    # Interactive submenu for managing patient records
    from patientRecords.record import PatientRecordManager
    from Users.Doctors import Doctor
    import json

    manager = PatientRecordManager()

    # Seed at least one doctor (try loading from doctor_1.json if present)
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        doctor_json = os.path.join(project_root, "doctor_1.json")
        if os.path.exists(doctor_json):
            with open(doctor_json, "r") as f:
                data = json.load(f)
            doc = Doctor(
                DoctorID=data.get("DoctorID", 1),
                Name=data.get("Name", "Dr. Smith"),
                daysWorking=data.get("daysWorking", {})
            )
            # Migrate any legacy weekday-name keys to date keys
            try:
                doc.migrate_legacy_day_keys()
                # Persist migrated schedule
                doc.save_to_json(doctor_json)
            except Exception:
                pass
            manager.add_doctor(doc)
        else:
            manager.add_doctor(Doctor(DoctorID=1, Name="Dr. Smith", daysWorking={}))
    except Exception:
        manager.add_doctor(Doctor(DoctorID=1, Name="Dr. Smith", daysWorking={}))

    def pick_doctor():
        # Helper to select a doctor, defaults to the first available
        if not manager.doctors:
            return Doctor(DoctorID=1, Name="Dr. Smith", daysWorking={})
        print("Available doctors:")
        for did, doc in manager.doctors.items():
            print(f"- {did}: {getattr(doc, 'Name', 'Unknown')}")
        try:
            did = int(input("Enter DoctorID: ").strip())
            return manager.doctors.get(did) or next(iter(manager.doctors.values()))
        except Exception:
            return next(iter(manager.doctors.values()))

    while True:
        print("\nPatient Records")
        print("1. Add record")
        print("2. Update record")
        print("3. Sort records")
        print("4. View records")
        print("5. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            # Add a new record
            record = {}
            record['recordID'] = input("Record ID: ").strip()
            record['Date'] = input("Date (YYYY-MM-DD): ").strip()
            record['Time'] = input("Time (HH:MM): ").strip()
            record['Patient'] = input("Patient name: ").strip()
            record['Doctor'] = pick_doctor()  # Pass Doctor object to avoid None issues
            record['Symptoms'] = input("Symptoms: ").strip()
            record['Diagnosis'] = input("Diagnosis: ").strip()
            record['Treatment'] = input("Treatment: ").strip()
            record['Medication'] = input("Medication: ").strip()
            record['results'] = input("Results: ").strip()
            record['notes'] = input("Notes: ").strip()
            manager.add_record(record)
            print("Record added.")
        elif choice == "2":
            # Update an existing record
            rid = input("Record ID to update: ").strip()
            updated = {}
            print("Leave blank to keep current value.")
            val = input("New Date (YYYY-MM-DD): ").strip()
            if val:
                updated['Date'] = val
            val = input("New Time (HH:MM): ").strip()
            if val:
                updated['Time'] = val
            val = input("New Patient: ").strip()
            if val:
                updated['Patient'] = val
            change_doc = input("Change Doctor? (y/N): ").strip().lower()
            if change_doc == 'y':
                updated['Doctor'] = pick_doctor()
            val = input("New Symptoms: ").strip()
            if val:
                updated['Symptoms'] = val
            val = input("New Diagnosis: ").strip()
            if val:
                updated['Diagnosis'] = val
            val = input("New Treatment: ").strip()
            if val:
                updated['Treatment'] = val
            val = input("New Medication: ").strip()
            if val:
                updated['Medication'] = val
            val = input("New Results: ").strip()
            if val:
                updated['results'] = val
            val = input("New Notes: ").strip()
            if val:
                updated['notes'] = val
            if manager.update_record(rid, updated):
                print("Record updated.")
            else:
                print("Record ID not found.")
        elif choice == "3":
            # Sort records by selected key
            print("Sort by:")
            print("1. Date")
            print("2. Patient")
            sel = input("Enter choice: ").strip()
            if sel == "2":
                manager.sort_records(key=lambda x: x.get('Patient', ''))
            else:
                manager.sort_records(key=lambda x: x.get('Date', ''))
            print("Records sorted.")
        elif choice == "4":
            print(manager.view_records())
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

def manage_medical_history():
    from medicalHistory.heap_sort import heap_sort
    import json

    # Persist data in a JSON file at the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    hist_json = os.path.join(project_root, "medical_histories.json")

    histories = []

    # Load existing histories if present
    if os.path.exists(hist_json):
        try:
            with open(hist_json, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    histories = data
        except Exception as e:
            print(f"Warning: could not load histories: {e}")

    def save():
        try:
            with open(hist_json, "w") as f:
                json.dump(histories, f, indent=4)
        except Exception as e:
            print(f"Warning: could not save histories: {e}")

    def to_int(val, default=0):
        try:
            return int(val)
        except Exception:
            return default

    while True:
        print("\nMedical History")
        print("1. Add history entry")
        print("2. Update history entry")
        print("3. Sort histories by date")
        print("4. View histories")
        print("5. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            entry = {}
            entry['historyID'] = input("History ID: ").strip()
            entry['date'] = input("Date (YYYY-MM-DD): ").strip()
            entry['patient'] = input("Patient name: ").strip()
            entry['doctor'] = input("Doctor name: ").strip()
            entry['age'] = to_int(input("Patient age: ").strip() or 0)
            diag = input("Diagnosis (comma-separated): ").strip()
            inj = input("Injuries (comma-separated): ").strip()
            meds = input("Medications (comma-separated): ").strip()
            alg = input("Allergies (comma-separated): ").strip()
            entry['diagnosis'] = [s.strip() for s in diag.split(',') if s.strip()]
            entry['injuries'] = [s.strip() for s in inj.split(',') if s.strip()]
            entry['medications'] = [s.strip() for s in meds.split(',') if s.strip()]
            entry['allergies'] = [s.strip() for s in alg.split(',') if s.strip()]
            histories.append(entry)
            save()
            print("History added.")
        elif choice == "2":
            hid = input("History ID to update: ").strip()
            entry = next((h for h in histories if h.get('historyID') == hid), None)
            if not entry:
                print("History ID not found.")
                continue
            print("Leave blank to keep current value.")
            val = input(f"New Date (YYYY-MM-DD) [{entry.get('date','')}]: ").strip()
            if val:
                entry['date'] = val
            val = input(f"New Patient [{entry.get('patient','')}]: ").strip()
            if val:
                entry['patient'] = val
            val = input(f"New Doctor [{entry.get('doctor','')}]: ").strip()
            if val:
                entry['doctor'] = val
            val = input(f"New Age [{entry.get('age',0)}]: ").strip()
            if val:
                entry['age'] = to_int(val, entry.get('age', 0))
            val = input("New Diagnosis (comma-separated): ").strip()
            if val:
                entry['diagnosis'] = [s.strip() for s in val.split(',') if s.strip()]
            val = input("New Injuries (comma-separated): ").strip()
            if val:
                entry['injuries'] = [s.strip() for s in val.split(',') if s.strip()]
            val = input("New Medications (comma-separated): ").strip()
            if val:
                entry['medications'] = [s.strip() for s in val.split(',') if s.strip()]
            val = input("New Allergies (comma-separated): ").strip()
            if val:
                entry['allergies'] = [s.strip() for s in val.split(',') if s.strip()]
            save()
            print("History updated.")
        elif choice == "3":
            try:
                heap_sort(histories)  # sorts in-place by 'date'
                save()
                print("Histories sorted by date.")
            except Exception as e:
                print(f"Failed to sort histories: {e}")
        elif choice == "4":
            if not histories:
                print("No medical histories available.")
            else:
                for h in histories:
                    print(
                        f"ID: {h.get('historyID','')}, Date: {h.get('date','')}, "
                        f"Patient: {h.get('patient','')}, Doctor: {h.get('doctor','')}, Age: {h.get('age','')}\n"
                        f"  Diagnosis: {', '.join(h.get('diagnosis', []))}\n"
                        f"  Injuries: {', '.join(h.get('injuries', []))}\n"
                        f"  Medications: {', '.join(h.get('medications', []))}\n"
                        f"  Allergies: {', '.join(h.get('allergies', []))}"
                    )
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

def schedule_appointments(current_user):
    from appointmentSchedule.merge_sort import merge_sort
    from Users.Doctors import Doctor
    import json
    from datetime import datetime

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    appts_json = os.path.join(project_root, "appointments.json")
    doctor_json = os.path.join(project_root, "doctor_1.json")

    # Load or create doctor
    doctor = None
    try:
        if os.path.exists(doctor_json):
            doctor = Doctor.load_from_json(doctor_json)
        if not doctor:
            doctor = Doctor(DoctorID=1, Name="Dr. Smith", daysWorking={})
        else:
            # Migrate any legacy weekday-name keys to concrete date keys
            try:
                doctor.migrate_legacy_day_keys()
                doctor.save_to_json(doctor_json)
            except Exception:
                pass
    except Exception:
        doctor = Doctor(DoctorID=1, Name="Dr. Smith", daysWorking={})

    # Load appointments
    appointments = []
    if os.path.exists(appts_json):
        try:
            with open(appts_json, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    appointments = data
        except Exception as e:
            print(f"Warning: could not load appointments: {e}")

    def save_appointments():
        try:
            with open(appts_json, "w") as f:
                json.dump(appointments, f, indent=4)
        except Exception as e:
            print(f"Warning: could not save appointments: {e}")

    def save_doctor():
        try:
            doctor.save_to_json(doctor_json)
        except Exception as e:
            print(f"Warning: could not save doctor schedule: {e}")

    def to_int(val, default=0):
        try:
            return int(val)
        except Exception:
            return default

    def parse_date(date_str):
        try:
            # Validate format and return normalized YYYY-MM-DD
            dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d"), dt
        except Exception:
            return None, None

    def ensure_date_in_schedule(date_str):
        # If date not present, seed default weekday hours (Mon-Fri: 9,10,11,13,14,15,16)
        if date_str not in doctor.daysWorking:
            _, dt = parse_date(date_str)
            if not dt:
                return False
            if dt.weekday() < 5:  # 0=Mon .. 4=Fri
                default_hours = [9, 10, 11, 13, 14, 15, 16]
                doctor.daysWorking[date_str] = [default_hours[:], []]
                save_doctor()
                return True
            else:
                # Weekends: no working hours by default
                doctor.daysWorking[date_str] = [[], []]
                save_doctor()
                return True
        return True

    def available_slots(date_str):
        ok = ensure_date_in_schedule(date_str)
        if not ok:
            return []
        work, booked = doctor.daysWorking.get(date_str, [[], []])
        avail = [{"time": h} for h in work if h not in booked]
        sorted_avail = merge_sort(avail)
        return [s["time"] for s in sorted_avail]

    def next_id():
        try:
            return max(int(a.get("appointmentID", 0)) for a in appointments) + 1 if appointments else 1
        except Exception:
            return len(appointments) + 1

    while True:
        print("\nAppointments")
        print("1. View available slots")
        print("2. Schedule appointment")
        print("3. Cancel appointment")
        print("4. Reschedule appointment")
        print("5. View appointments")
        print("6. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            date_in = input("Enter date (YYYY-MM-DD): ").strip()
            norm, _ = parse_date(date_in)
            if not norm:
                print("Invalid date format. Use YYYY-MM-DD.")
                continue
            slots = available_slots(norm)
            if not slots:
                print("No available slots for that date.")
            else:
                print("Available hours:", ", ".join(str(s) for s in slots))
        elif choice == "2":
            patient = input("Patient name: ").strip()
            date_in = input("Date (YYYY-MM-DD): ").strip()
            norm, _ = parse_date(date_in)
            if not norm:
                print("Invalid date format.")
                continue
            slots = available_slots(norm)
            if not slots:
                print("No available slots for that date.")
                continue
            print("Available hours:", ", ".join(str(s) for s in slots))
            try:
                hour = int(input("Choose hour: ").strip())
            except Exception:
                print("Invalid hour.")
                continue
            if not doctor.checkAvailability(norm, hour):
                print("Selected time is not available.")
                continue
            if not doctor.bookHour(norm, hour):
                print("Failed to book the slot.")
                continue
            appt = {
                "appointmentID": next_id(),
                "patient": patient,
                "doctorID": doctor.DoctorID,
                "doctorName": doctor.Name,
                "date": norm,
                "time": hour
            }
            appointments.append(appt)
            save_appointments()
            save_doctor()
            print("Appointment scheduled.")
        elif choice == "3":
            # Only doctors and admins can cancel any appointment
            if not current_user.has_permission(Roles.DOCTOR):
                print("Access denied. Requires doctor or admin.")
                continue
            try:
                appt_id = int(input("Appointment ID to cancel: ").strip())
            except Exception:
                print("Invalid ID.")
                continue
            appt = next((a for a in appointments if int(a.get("appointmentID", -1)) == appt_id), None)
            if not appt:
                print("Appointment not found.")
                continue
            date_key = appt.get("date") or appt.get("day")  # backward compatibility
            t = to_int(appt.get("time", 0), 0)
            if date_key in doctor.daysWorking:
                try:
                    if t in doctor.daysWorking[date_key][1]:
                        doctor.daysWorking[date_key][1].remove(t)
                except Exception:
                    pass
            appointments = [a for a in appointments if int(a.get("appointmentID", -1)) != appt_id]
            save_appointments()
            save_doctor()
            print("Appointment canceled.")
        elif choice == "4":
            # Only doctors and admins can reschedule any appointment
            if not current_user.has_permission(Roles.DOCTOR):
                print("Access denied. Requires doctor or admin.")
                continue
            try:
                appt_id = int(input("Appointment ID to reschedule: ").strip())
            except Exception:
                print("Invalid ID.")
                continue
            appt = next((a for a in appointments if int(a.get("appointmentID", -1)) == appt_id), None)
            if not appt:
                print("Appointment not found.")
                continue
            old_date = (appt.get("date") or appt.get("day") or "").strip()
            old_time = to_int(appt.get("time", 0), 0)
            new_date_in = input("New date (YYYY-MM-DD): ").strip()
            new_date, _ = parse_date(new_date_in)
            if not new_date:
                print("Invalid date format.")
                continue
            slots = available_slots(new_date)
            if not slots:
                print("No available slots for that date.")
                continue
            print("Available hours:", ", ".join(str(s) for s in slots))
            try:
                new_time = int(input("New hour: ").strip())
            except Exception:
                print("Invalid hour.")
                continue
            if not doctor.checkAvailability(new_date, new_time):
                print("Selected new time is not available.")
                continue
            try:
                if old_date in doctor.daysWorking and old_time in doctor.daysWorking[old_date][1]:
                    doctor.daysWorking[old_date][1].remove(old_time)
            except Exception:
                pass
            if not doctor.bookHour(new_date, new_time):
                print("Failed to book new slot.")
                continue
            appt["date"], appt["time"] = new_date, new_time
            if "day" in appt:
                appt.pop("day", None)
            save_appointments()
            save_doctor()
            print("Appointment rescheduled.")
        elif choice == "5":
            if not appointments:
                print("No appointments scheduled.")
            else:
                by_date = {}
                for a in appointments:
                    key = a.get("date") or a.get("day") or ""
                    by_date.setdefault(key, []).append({"time": to_int(a.get("time", 0), 0), "_a": a})
                for date_key in sorted(by_date.keys()):
                    day_list = merge_sort(by_date[date_key])
                    print(f"\n{date_key}:")
                    for item in day_list:
                        a = item["_a"]
                        print(f"  ID {a.get('appointmentID')}: {item.get('time')}:00 - {a.get('patient')} with {a.get('doctorName')}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()