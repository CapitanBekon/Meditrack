class patient:
    def __init__(self, Name, lastName, DOB ,PatientID, Email, PhoneNumber, Address,Username, Password, permissionLevel, accountCreated):
        self.Name = Name
        self.lastName = lastName
        self.DOB = DOB
        self.PatientID = PatientID
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        

    #Getters
    def getName(self):
        return self.Name
    def getlastName(self):
        return self.lastName
    def getDOB(self):
        return self.DOB
    def getPatientID(self):
        return self.PatientID
    def getEmail(self):
        return self.Email
    def getPhoneNumber(self):  
        return self.PhoneNumber
    def getAddress(self):
        return self.Address
    def getPermissionLevel(self):
        return self.permissionLevel


    #Setters
    def setName(self, new_name):
        self.Name = new_name
    def setlastName(self, new_lastName):
        self.lastName = new_lastName
    def setDOB(self, new_DOB):
        self.DOB = new_DOB
    def setPatientID(self, new_PatientID):
        self.PatientID = new_PatientID
    def setEmail(self, new_Email):
        self.Email = new_Email
    def setPhoneNumber(self, new_PhoneNumber):
        self.PhoneNumber = new_PhoneNumber
    def setAddress(self, new_Address):
        self.Address = new_Address

    def ViewMedicalHistory(self):
        # Logic to view medical history
        pass