import sys
import os
from Users.User import User  # Import the User class for login functionality

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add the src directory to the system path

# Predefined users for the login system (for demonstration purposes)
users = {
    "admin": User(user_id="1", username="admin", password="admin123", permission_level=3, accountCreated=0),
    "doctor": User(user_id="2", username="doctor", password="doctor123", permission_level=2, accountCreated=0),
    "patient": User(user_id="3", username="patient", password="patient123", permission_level=1, accountCreated=0),
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
            manage_patient_records()
        elif choice == '2':
            manage_medical_history()
        elif choice == '3':
            schedule_appointments()
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
        if user and user.login(username, password):
            return user
        print("Invalid username or password. Please try again.")
    
    print("Too many failed login attempts.")
    return None

def manage_patient_records():
    from patientRecords.quick_sort import quick_sort  # Corrected import path
    # Implementation for managing patient records goes here
    print("Managing patient records...")

def manage_medical_history():
    from medicalHistory.heap_sort import heap_sort  # Corrected import path
    # Implementation for managing medical history goes here
    print("Managing medical history...")

def schedule_appointments():
    from appointmentSchedule.merge_sort import merge_sort  # Corrected import path
    # Implementation for scheduling appointments goes here
    print("Scheduling appointments...")

if __name__ == "__main__":
    main()