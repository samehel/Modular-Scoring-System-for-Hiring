import uuid
from typing import List

from questions.domain.interfaces.question_generator import QuestionGenerator
from questions.domain.entities.question_entities import MCQQuestionEntity
from questions.domain.value_objects.question_type import QuestionType

MCQ_TEMPLATES = {
    "data_structures": {
        "EASY": [
            {
                "title": "What is an Array?",
                "description": "Basic data structure question.",
                "choices": [
                    "A collection of elements stored at contiguous memory locations",
                    "A linked list of elements",
                    "A key-value store",
                    "A tree structure",
                ],
                "correct_answer": "A collection of elements stored at contiguous memory locations",
            },
            {
                "title": "Stack Behaviour",
                "description": "Which principle does a stack follow?",
                "choices": ["FIFO", "LIFO", "Random Access", "Priority-based"],
                "correct_answer": "LIFO",
            },
        ],
        "MEDIUM": [
            {
                "title": "Hash Table Collision",
                "description": "Which technique resolves hash collisions using a linked list?",
                "choices": ["Open Addressing", "Separate Chaining", "Double Hashing", "Linear Probing"],
                "correct_answer": "Separate Chaining",
            },
        ],
        "HARD": [
            {
                "title": "Red-Black Tree Property",
                "description": "Which of the following is NOT a property of a Red-Black Tree?",
                "choices": [
                    "Root is always black",
                    "No two consecutive red nodes",
                    "All leaves (NIL) are red",
                    "Both children of a red node are black",
                ],
                "correct_answer": "All leaves (NIL) are red",
            },
        ],
    },
    "algorithms": {
        "EASY": [
            {
                "title": "Binary Search Prerequisite",
                "description": "What is required before applying binary search?",
                "choices": ["The array must be sorted", "The array must be unsorted", "The array must have even length", "The array must contain unique elements"],
                "correct_answer": "The array must be sorted",
            },
        ],
        "MEDIUM": [
            {
                "title": "QuickSort Complexity",
                "description": "What is the average-case time complexity of QuickSort?",
                "choices": ["O(n²)", "O(n log n)", "O(log n)", "O(n)"],
                "correct_answer": "O(n log n)",
            },
        ],
        "HARD": [
            {
                "title": "P vs NP",
                "description": "Which problem is in NP-Complete?",
                "choices": ["Binary Search", "Merge Sort", "Travelling Salesman Problem", "BFS"],
                "correct_answer": "Travelling Salesman Problem",
            },
        ],
    },
    "python": {
        "EASY": [
            {
                "title": "Python List Comprehension",
                "description": "What does [x**2 for x in range(5)] produce?",
                "choices": ["[0,1,4,9,16]", "[1,2,3,4,5]", "[0,1,2,3,4]", "[1,4,9,16,25]"],
                "correct_answer": "[0,1,4,9,16]",
            },
        ],
        "MEDIUM": [
            {
                "title": "Python GIL",
                "description": "What does Python's GIL prevent?",
                "choices": [
                    "Running I/O operations",
                    "True parallel execution of Python bytecode in threads",
                    "Using multiple processes",
                    "Using async/await",
                ],
                "correct_answer": "True parallel execution of Python bytecode in threads",
            },
        ],
        "HARD": [
            {
                "title": "Python Metaclass",
                "description": "What is the default metaclass in Python?",
                "choices": ["object", "type", "meta", "class"],
                "correct_answer": "type",
            },
        ],
    },
}


class MCQQuestionGenerator(QuestionGenerator):
    """Generates MCQQuestionEntity objects from hardcoded topic templates."""

    def generate(self, topic: str, difficulty: str, count: int) -> List[MCQQuestionEntity]:
        topic_lower = topic.lower()
        difficulty_upper = difficulty.upper()

        templates = MCQ_TEMPLATES.get(topic_lower, {}).get(difficulty_upper, [])

        if not templates:
            all_templates = [t for sub in MCQ_TEMPLATES.get(topic_lower, {}).values() for t in sub]
            templates = all_templates

        if not templates:
            return []

        result = []
        for i in range(count):
            tmpl = templates[i % len(templates)]
            result.append(
                MCQQuestionEntity(
                    id=str(uuid.uuid4()),
                    title=tmpl["title"],
                    description=tmpl["description"],
                    difficulty=difficulty_upper,
                    topic=topic_lower,
                    question_type=QuestionType.MCQ.value,
                    choices=tmpl["choices"],
                    correct_answer=tmpl["correct_answer"],
                )
            )
        return result
