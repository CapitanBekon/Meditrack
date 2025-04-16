# Healthcare Management System

This project is a comprehensive Healthcare Management System designed to efficiently manage patient records, medical histories, and appointment scheduling. The system leverages various sorting algorithms to ensure that data is organized and easily accessible.

---

## Features

- **Patient Record Management**: 
  - Implements the **Quick Sort** algorithm to manage and sort patient records based on criteria such as date of birth or last visit.
  - Allows adding, updating, and viewing patient records.
  
- **Medical History Management**: 
  - Utilizes the **Heap Sort** algorithm for managing and sorting medical history entries.
  - Supports adding, updating, and sorting medical histories by diagnosis, medications, or other criteria.

- **Appointment Scheduling**: 
  - Employs the **Merge Sort** algorithm for handling and sorting appointments based on time slots.
  - Includes features for scheduling, rescheduling, canceling, and viewing appointments.

---

## Project Structure

```
healthcare-management-system
├── src
│   ├── Users
│   │   ├── Doctors.py
│   │   ├── Patient.py
│   │   └── User.py
│   ├── patientRecords
│   │   ├── record.py
│   │   ├── quick_sort.py
│   │   └── __init__.py
│   ├── medicalHistory
│   │   ├── history.py
│   │   ├── heap_sort.py
│   │   └── __init__.py
│   ├── appointmentSchedule
│   │   ├── appointment.py
│   │   ├── merge_sort.py
│   │   └── __init__.py
│   ├── utils
│   │   └── __init__.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory**:
   ```bash
   cd healthcare-management-system
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

To run the application, execute the following command:
```bash
python src/main.py
```

### Available Features:
1. **Manage Patient Records**:
   - Add, update, and sort patient records.
   - Sort records by date of birth, last visit, or other criteria using Quick Sort.

2. **Manage Medical Histories**:
   - Add and update medical histories.
   - Sort histories by diagnosis, medications, or other fields using Heap Sort.

3. **Schedule Appointments**:
   - Schedule, reschedule, and cancel appointments.
   - Suggest available time slots for doctors.
   - Sort appointments by time using Merge Sort.

---

## Dependencies

The project requires the following Python libraries:
- **Flask**: For potential web-based extensions.
- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical computations.
- **pytest**: For testing the application.

Install them using:
```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear messages.
4. Submit a pull request for review.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For any questions or suggestions, please feel free to open an issue or contact the repository owner.