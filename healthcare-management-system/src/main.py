def main():
    print("Welcome to the Healthcare Management System")
    
    while True:
        print("\nSelect an option:")
        print("1. Manage Patient Records")
        print("2. Manage Medical History")
        print("3. Schedule Appointments")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            manage_patient_records()
        elif choice == '2':
            manage_medical_history()
        elif choice == '3':
            schedule_appointments()
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def manage_patient_records():
    from patient_records.quick_sort import quick_sort
    # Implementation for managing patient records goes here

def manage_medical_history():
    from medical_history.heap_sort import heap_sort
    # Implementation for managing medical history goes here

def schedule_appointments():
    from appointment_scheduling.merge_sort import merge_sort
    # Implementation for scheduling appointments goes here

if __name__ == "__main__":
    main()