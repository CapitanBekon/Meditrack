from typing import Dict, Union
from Users.User import User
from Users.Doctors import Doctor
from Users.Patient import patient

class Admin:
    def __init__(self):
        """
        Initialize the Admin class.
        """
        self.users = {}  # Dictionary to store users by their user_id

    def create_user(self, user_type: str, details: Dict) -> Union[User, None]:
        """
        Create a new user.
        :param user_type: The type of user to create (e.g., 'Doctor', 'Patient').
        :param details: A dictionary containing the details of the user.
        :return: The created User object or None if the user type is invalid.
        """
        if user_type == "Doctor":
            new_user = Doctor(
                DoctorID=details["DoctorID"],
                Name=details["Name"],
                daysWorking=details["daysWorking"]
            )
        elif user_type == "Patient":
            new_user = patient(
                Name=details["Name"],
                lastName=details["lastName"],
                DOB=details["DOB"],
                PatientID=details["PatientID"],
                Email=details["Email"],
                PhoneNumber=details["PhoneNumber"],
                Address=details["Address"],
                Username=details["Username"],
                Password=details["Password"],
                permissionLevel=details["permissionLevel"],
                accountCreated=True
            )
        else:
            print(f"Invalid user type: {user_type}")
            return None

        # Add the new user to the users dictionary
        self.users[details["ID"]] = new_user
        return new_user

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by their user ID.
        :param user_id: The ID of the user to delete.
        :return: True if the user was successfully deleted, False otherwise.
        """
        if user_id in self.users:
            del self.users[user_id]
            return True
        print(f"User with ID {user_id} not found.")
        return False

    def update_permissions(self, user_id: str, new_level: int) -> None:
        """
        Update the permission level of a user.
        :param user_id: The ID of the user whose permissions are to be updated.
        :param new_level: The new permission level to assign.
        """
        user = self.users.get(user_id)
        if user:
            user.permissionLevel = new_level
            print(f"Updated permissions for user {user_id} to level {new_level}.")
        else:
            print(f"User with ID {user_id} not found.")
