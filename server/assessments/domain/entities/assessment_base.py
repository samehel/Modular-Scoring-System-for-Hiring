from abc import ABC
from datetime import datetime

from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.value_objects.assessment_status import AssessmentStatus

class AssessmentBase(ABC):
    def __init__(self, id: str, name: str, description: str, 
                 type: AssessmentType, status: AssessmentStatus,
                 created_by: str, created_at: datetime, updated_at: datetime) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.status = status
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at    
        