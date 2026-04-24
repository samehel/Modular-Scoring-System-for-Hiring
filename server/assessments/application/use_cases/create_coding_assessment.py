"""
Phase 8 — Create Coding Assessment use case.
Generates questions from multiple topics, saves them to MongoDB,
and persists a CodingAssessment record with their IDs.
"""
import uuid
from datetime import datetime

from assessments.application.dtos.create_coding_assessment_dto import CreateCodingAssessmentDTO
from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.value_objects.assessment_status import AssessmentStatus
from users.domain.interfaces.user_repository import UserRepository
from questions.infrastructure.generators.coding_question_generator import CodingQuestionGenerator
from questions.models import CodingQuestion as CodingQuestionModel


class CreateCodingAssessmentUseCase:

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        user_repository: UserRepository,
    ) -> None:
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository

    def execute(self, dto: CreateCodingAssessmentDTO, user_id: str) -> dict:
        if not dto.name.strip():
            raise ValueError("Assessment name is required")
        if not dto.topics:
            raise ValueError("At least one topic is required")

        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Author not found")

        generator = CodingQuestionGenerator()
        questions_per_topic = max(1, dto.question_count // len(dto.topics))
        all_questions = []

        for topic in dto.topics:
            qs = generator.generate(topic, dto.difficulty, questions_per_topic)
            all_questions.extend(qs)

        # Persist questions in MongoDB and collect IDs
        question_ids = []
        for q in all_questions:
            model = CodingQuestionModel(
                id=q.id,
                title=q.title,
                description=q.description,
                difficulty=q.difficulty,
                topic=q.topic,
                question_type=q.question_type,
                problem_statement=q.problem_statement,
                test_cases=q.test_cases,
                solution_code=q.solution_code,
            )
            model.save()
            question_ids.append(q.id)

        # Create CodingAssessment model
        from assessments.models import CodingAssessment as CodingAssessmentModel
        from users.models import User as UserModel

        assessment_id = str(uuid.uuid4())
        assessment_model = CodingAssessmentModel(
            id=assessment_id,
            name=dto.name,
            description=dto.description,
            type=AssessmentType.CODING.name,
            status=AssessmentStatus.DRAFT.name,
            created_by=UserModel.objects(id=user_id).first(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            topics=dto.topics,
            difficulty=dto.difficulty,
            question_count=dto.question_count,
            time_limit=dto.time_limit,
            question_ids=question_ids,
        )
        assessment_model.save()

        return {
            "id": assessment_id,
            "name": dto.name,
            "description": dto.description,
            "type": "CODING",
            "status": "DRAFT",
            "topics": dto.topics,
            "difficulty": dto.difficulty,
            "question_count": len(question_ids),
            "time_limit": dto.time_limit,
            "questions": [
                {
                    "id": q.id,
                    "title": q.title,
                    "problem_statement": q.problem_statement,
                    "difficulty": q.difficulty,
                    "topic": q.topic,
                }
                for q in all_questions
            ],
        }
