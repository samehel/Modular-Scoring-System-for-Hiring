import uuid
from typing import List

from questions.domain.interfaces.question_generator import QuestionGenerator
from questions.domain.entities.question_entities import TextQuestionEntity
from questions.domain.value_objects.question_type import QuestionType

INTERVIEW_TEMPLATES = {
    "BEHAVIORAL": [
        {
            "title": "Tell me about yourself",
            "description": "General introduction question.",
            "keywords": ["experience", "background", "skills", "career"],
        },
        {
            "title": "Describe a challenge you overcame",
            "description": "Tests resilience and problem-solving.",
            "keywords": ["challenge", "obstacle", "resolved", "solution", "team"],
        },
        {
            "title": "Where do you see yourself in 5 years?",
            "description": "Tests ambition and planning.",
            "keywords": ["goals", "growth", "leadership", "career", "development"],
        },
        {
            "title": "How do you handle tight deadlines?",
            "description": "Tests time management and stress handling.",
            "keywords": ["deadline", "priority", "manage", "stress", "planning"],
        },
        {
            "title": "Describe a time you showed leadership",
            "description": "Tests leadership skills.",
            "keywords": ["lead", "team", "initiative", "decision", "responsibility"],
        },
    ],
    "TECHNICAL": [
        {
            "title": "Explain the difference between REST and GraphQL",
            "description": "Tests API knowledge.",
            "keywords": ["REST", "GraphQL", "endpoint", "query", "schema", "flexibility"],
        },
        {
            "title": "What is a race condition?",
            "description": "Tests concurrency knowledge.",
            "keywords": ["concurrency", "thread", "mutex", "synchronization", "race"],
        },
        {
            "title": "Explain CAP theorem",
            "description": "Tests distributed systems knowledge.",
            "keywords": ["consistency", "availability", "partition", "distributed", "trade-off"],
        },
        {
            "title": "What is dependency injection?",
            "description": "Tests software design patterns knowledge.",
            "keywords": ["inversion", "control", "dependency", "inject", "decouple"],
        },
        {
            "title": "How does HTTPS work?",
            "description": "Tests networking and security knowledge.",
            "keywords": ["TLS", "certificate", "handshake", "encryption", "SSL"],
        },
    ],
    "EXPERIENCE": [
        {
            "title": "What technologies have you worked with most recently?",
            "description": "Tests recency of technical experience.",
            "keywords": ["language", "framework", "tool", "stack", "project"],
        },
        {
            "title": "Describe your most challenging project",
            "description": "Tests depth of real experience.",
            "keywords": ["complex", "project", "architecture", "scale", "delivered"],
        },
        {
            "title": "How many years of experience do you have in your primary stack?",
            "description": "Tests specific domain experience.",
            "keywords": ["years", "experience", "proficiency", "primary", "expertise"],
        },
    ],
    "EDUCATION": [
        {
            "title": "What is your highest level of education?",
            "description": "Tests formal education background.",
            "keywords": ["degree", "bachelor", "master", "PhD", "university"],
        },
        {
            "title": "Have you completed any relevant certifications?",
            "description": "Tests professional certifications.",
            "keywords": ["certification", "AWS", "Google", "certified", "professional"],
        },
        {
            "title": "Did your degree involve practical project work?",
            "description": "Tests applied education.",
            "keywords": ["project", "practical", "thesis", "applied", "capstone"],
        },
    ],
}


class InterviewQuestionGenerator(QuestionGenerator):
    """Generates TextQuestionEntity objects from hardcoded category templates."""

    def generate(self, topic: str, difficulty: str, count: int) -> List[TextQuestionEntity]:
        # For interview questions, `topic` maps to category
        category_upper = topic.upper()
        templates = INTERVIEW_TEMPLATES.get(category_upper, [])

        if not templates:
            # Fall back to all interview questions
            templates = [t for sub in INTERVIEW_TEMPLATES.values() for t in sub]

        result = []
        for i in range(count):
            tmpl = templates[i % len(templates)]
            result.append(
                TextQuestionEntity(
                    id=str(uuid.uuid4()),
                    title=tmpl["title"],
                    description=tmpl["description"],
                    difficulty=difficulty.upper(),
                    topic=category_upper.lower(),
                    question_type=QuestionType.TEXT.value,
                    category=category_upper,
                    keywords=tmpl.get("keywords", []),
                )
            )
        return result
