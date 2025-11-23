
class RegisterAdminDto():
    def __init__(self, email: str, password: str, company_name: str, industry: str):
        self.email = email
        self.password = password
        self.company_name = company_name
        self.industry = industry

