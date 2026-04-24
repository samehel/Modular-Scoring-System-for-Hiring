"""Phase 12 — Create Interview Assessment use case."""
import uuid
from datetime import datetime

from assessments.application.dtos.create_interview_assessment_dto import CreateInterviewAssessmentDTO
from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.value_objects.assessment_status import AssessmentStatus
from users.domain.interfaces.user_repository import UserRepository
from questions.infrastructure.generators.interview_question_generator import InterviewQuestionGenerator
from questions.models import TextQuestion as TextQuestionModel


class CreateInterviewAssessmentUseCase:

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        user_repository: UserRepository,
    ) -> None:
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository

    def execute(self, dto: CreateInterviewAssessmentDTO, user_id: str) -> dict:
        if not dto.name.strip():
            raise ValueError("Assessment name is required")
        if not dto.categories:
            raise ValueError("At least one category is required")

        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Author not found")

        generator = InterviewQuestionGenerator()
        per_cat = max(1, dto.question_count // len(dto.categories))
        all_questions = []

        for category in dto.categories:
            qs = generator.generate(category, "MEDIUM", per_cat)
            all_questions.extend(qs)

        question_ids = []
        for q in all_questions:
            model = TextQuestionModel(
                id=q.id,
                title=q.title,
                description=q.description,
                difficulty=q.difficulty,
                topic=q.topic,
                question_type=q.question_type,
                category=q.category,
                keywords=q.keywords,
            )
            model.save()
            question_ids.append(q.id)

        from assessments.models import InterviewAssessment as InterviewAssessmentModel
        from users.models import User as UserModel

        assessment_id = str(uuid.uuid4())
        assessment_model = InterviewAssessmentModel(
            id=assessment_id,
            name=dto.name,
            description=dto.description,
            type=AssessmentType.INTERVIEW.name,
            status=AssessmentStatus.DRAFT.name,
            created_by=UserModel.objects(id=user_id).first(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            categories=dto.categories,
            time_limit=dto.time_limit,
            question_count=dto.question_count,
            question_ids=question_ids,
        )
        assessment_model.save()

        return {
            "id": assessment_id,
            "name": dto.name,
            "type": "INTERVIEW",
            "status": "DRAFT",
            "categories": dto.categories,
            "time_limit": dto.time_limit,
            "question_count": len(question_ids),
            "questions": [
                {"id": q.id, "title": q.title, "category": q.category}
                for q in all_questions
            ],
        }
