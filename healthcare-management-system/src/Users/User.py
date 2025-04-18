class User:
    def __init__(self, user_id: str, username: str, password: str, permission_level: int, accountCreated: float):
        """
        Initialize a User object.
        :param user_id: Unique identifier for the user.
        :param username: Username of the user.
        :param password: Password of the user.
        :param permission_level: Permission level of the user.
        """
        self.user_id = user_id
        self.username = username
        self.password = password
        self.permission_level = permission_level
        self.accountCreated = accountCreated  # Timestamp of when the account was created
        self.logged_in = False  # Tracks whether the user is logged in

    def login(self, username: str, password: str) -> bool:
        """
        Log in the user by verifying the username and password.
        :param username: The username entered by the user.
        :param password: The password entered by the user.
        :return: True if login is successful, False otherwise.
        """
        if self.username == username and self.password == password:
            self.logged_in = True
            print(f"User {self.username} logged in successfully.")
            return True
        print("Invalid username or password.")
        return False

    def logout(self) -> None:
        """
        Log out the user.
        """
        if self.logged_in:
            self.logged_in = False
            print(f"User {self.username} logged out successfully.")
        else:
            print(f"User {self.username} is not logged in.")

    def update_password(self, old_password: str, new_password: str) -> bool:
        """
        Update the user's password.
        :param old_password: The current password of the user.
        :param new_password: The new password to set.
        :return: True if the password was successfully updated, False otherwise.
        """
        if self.password == old_password:
            self.password = new_password
            print("Password updated successfully.")
            return True
        print("Old password is incorrect.")
        return False

    def get_permission_level(self) -> int:
        """
        Get the user's permission level.
        :return: The permission level of the user.
        """
        return self.permission_level