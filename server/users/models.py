from datetime import datetime
from mongoengine import *

from users.domain.value_objects.user_type import UserType

# Create your models here.

class User(Document):
    id = StringField(primary_key=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    user_type = EnumField(UserType)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

class AdminProfile(Document):
    user = ReferenceField(User, required=True, unique=True)
    company_name = StringField(required=True)
    industry = StringField(required=True)

class CandidateProfile(Document):
    user = ReferenceField(User, required=True, unique=True)
    phone = StringField(required=True)
    date_of_birth = DateField(required=True)