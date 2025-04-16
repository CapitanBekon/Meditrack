class User:
    def __init__(self, user_id, username, password, permission_level):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.is_authenticated = False
        self.permission_level = int

    def authenticate(self, password):
        #authentication logic

    def login(self):
        self.is_authenticated = False
        #Logic to log out the user