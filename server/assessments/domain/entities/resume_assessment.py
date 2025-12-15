
import datetime
from assessments.domain.entities.assessment_base import AssessmentBase
from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.value_objects.assessment_status import AssessmentStatus

class ResumeAssessment(AssessmentBase):
    def __init__(self, id: str, name: str, description: str, 
                    type: AssessmentType, status: AssessmentStatus, created_by: str, 
                    created_at: datetime, updated_at: datetime, criteria: list) -> None:
        super().__init__(id, name, description, type, status, 
                         created_by, created_at, updated_at)
        self.criteria = criteria
        
