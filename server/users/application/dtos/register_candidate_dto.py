from datetime import date

class RegisterCandidateDto():
    def __init__(self, email: str, password: str, phone: str, date_of_birth: date):
        self.email = email
        self.password = password
        self.phone = phone
        self.date_of_birth = date_of_birth
