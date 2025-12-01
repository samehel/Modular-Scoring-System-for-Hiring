
import datetime
from server.assessments.domain.entities.assessment_base import AssessmentBase


class ResumeAssessment(AssessmentBase):
    def __init__(self, id: str, name: str, description: str, 
                    type: AssessmentType, status: AssessmentStatus, created_by: str, 
                    created_at: datetime, updated_at: datetime, criteria: list) -> None:
        super().__init__(id, name, description, type, status, 
                         created_by, created_at, updated_at)
        self.criteria = criteria
        
