import uuid
from typing import List

from questions.domain.interfaces.question_generator import QuestionGenerator
from questions.domain.entities.question_entities import CodingQuestionEntity
from questions.domain.value_objects.question_type import QuestionType

# Template bank — topic → difficulty → list of question templates
CODING_TEMPLATES = {
    "arrays": {
        "EASY": [
            {
                "title": "Find Maximum Element",
                "description": "Write a function that returns the maximum element in an array.",
                "problem_statement": "Given an integer array, return the largest element.",
                "test_cases": [
                    {"input": "[3, 1, 4, 1, 5, 9]", "expected_output": "9"},
                    {"input": "[1]", "expected_output": "1"},
                    {"input": "[-5, -1, -3]", "expected_output": "-1"},
                ],
            },
            {
                "title": "Two Sum",
                "description": "Find two indices whose values add up to a target.",
                "problem_statement": "Given an array nums and integer target, return indices of two numbers that add up to target.",
                "test_cases": [
                    {"input": "nums=[2,7,11,15], target=9", "expected_output": "[0,1]"},
                    {"input": "nums=[3,2,4], target=6", "expected_output": "[1,2]"},
                ],
            },
        ],
        "MEDIUM": [
            {
                "title": "Subarray with Maximum Sum",
                "description": "Implement Kadane's algorithm to find the subarray with the largest sum.",
                "problem_statement": "Given an integer array, find the contiguous subarray with the largest sum and return its sum.",
                "test_cases": [
                    {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"},
                    {"input": "[1]", "expected_output": "1"},
                ],
            },
        ],
        "HARD": [
            {
                "title": "Merge k Sorted Arrays",
                "description": "Merge k sorted arrays into one sorted array efficiently.",
                "problem_statement": "Given k sorted arrays, merge them into a single sorted array.",
                "test_cases": [
                    {"input": "[[1,4,7],[2,5,8],[3,6,9]]", "expected_output": "[1,2,3,4,5,6,7,8,9]"},
                ],
            },
        ],
    },
    "strings": {
        "EASY": [
            {
                "title": "Reverse a String",
                "description": "Reverse the characters in a string.",
                "problem_statement": "Given a string s, return s reversed.",
                "test_cases": [
                    {"input": '"hello"', "expected_output": '"olleh"'},
                    {"input": '"abcde"', "expected_output": '"edcba"'},
                ],
            },
            {
                "title": "Check Palindrome",
                "description": "Determine if a string reads the same forwards and backwards.",
                "problem_statement": "Given a string, return True if it is a palindrome, False otherwise.",
                "test_cases": [
                    {"input": '"racecar"', "expected_output": "True"},
                    {"input": '"hello"', "expected_output": "False"},
                ],
            },
        ],
        "MEDIUM": [
            {
                "title": "Longest Substring Without Repeating Characters",
                "description": "Find the length of the longest substring without repeated characters.",
                "problem_statement": "Given a string s, find the length of the longest substring without repeating characters.",
                "test_cases": [
                    {"input": '"abcabcbb"', "expected_output": "3"},
                    {"input": '"bbbbb"', "expected_output": "1"},
                ],
            },
        ],
        "HARD": [
            {
                "title": "Minimum Window Substring",
                "description": "Find the smallest window containing all characters of a target string.",
                "problem_statement": "Given strings s and t, return the minimum window substring of s that contains all characters of t.",
                "test_cases": [
                    {"input": 's="ADOBECODEBANC", t="ABC"', "expected_output": '"BANC"'},
                ],
            },
        ],
    },
    "dynamic_programming": {
        "EASY": [
            {
                "title": "Fibonacci Number",
                "description": "Compute the nth Fibonacci number using dynamic programming.",
                "problem_statement": "Given n, return the nth Fibonacci number (0-indexed).",
                "test_cases": [
                    {"input": "5", "expected_output": "5"},
                    {"input": "10", "expected_output": "55"},
                ],
            },
        ],
        "MEDIUM": [
            {
                "title": "Coin Change",
                "description": "Find the fewest coins to make up an amount.",
                "problem_statement": "Given coins of different denominations and an amount, compute the fewest number of coins needed.",
                "test_cases": [
                    {"input": "coins=[1,5,11], amount=15", "expected_output": "3"},
                    {"input": "coins=[2], amount=3", "expected_output": "-1"},
                ],
            },
        ],
        "HARD": [
            {
                "title": "Edit Distance",
                "description": "Find the minimum edit distance between two strings.",
                "problem_statement": "Given two strings word1 and word2, return the minimum number of operations (insert, delete, replace) to convert word1 to word2.",
                "test_cases": [
                    {"input": 'word1="horse", word2="ros"', "expected_output": "3"},
                ],
            },
        ],
    },
    "sorting": {
        "EASY": [
            {
                "title": "Bubble Sort",
                "description": "Implement bubble sort algorithm.",
                "problem_statement": "Sort an integer array using bubble sort.",
                "test_cases": [
                    {"input": "[64,34,25,12,22,11,90]", "expected_output": "[11,12,22,25,34,64,90]"},
                ],
            },
        ],
        "MEDIUM": [
            {
                "title": "Merge Sort",
                "description": "Implement merge sort.",
                "problem_statement": "Sort an array using merge sort and return the sorted array.",
                "test_cases": [
                    {"input": "[38,27,43,3,9,82,10]", "expected_output": "[3,9,10,27,38,43,82]"},
                ],
            },
        ],
        "HARD": [
            {
                "title": "Sort Colors (Dutch National Flag)",
                "description": "Sort an array of 0s, 1s, and 2s in-place.",
                "problem_statement": "Sort an array containing only 0, 1, 2 in O(n) time with O(1) space.",
                "test_cases": [
                    {"input": "[2,0,2,1,1,0]", "expected_output": "[0,0,1,1,2,2]"},
                ],
            },
        ],
    },
    "graphs": {
        "EASY": [
            {
                "title": "BFS Traversal",
                "description": "Implement breadth-first search on a graph.",
                "problem_statement": "Given an adjacency list and a start node, return the BFS traversal order.",
                "test_cases": [
                    {"input": "graph={0:[1,2],1:[3],2:[4],3:[],4:[]}, start=0", "expected_output": "[0,1,2,3,4]"},
                ],
            },
        ],
        "MEDIUM": [
            {
                "title": "Number of Islands",
                "description": "Count the number of islands in a 2D grid.",
                "problem_statement": "Given a 2D grid of '1' (land) and '0' (water), return the number of islands.",
                "test_cases": [
                    {"input": '[["1","1","0","0"],["1","1","0","0"],["0","0","1","0"],["0","0","0","1"]]', "expected_output": "3"},
                ],
            },
        ],
        "HARD": [
            {
                "title": "Dijkstra's Shortest Path",
                "description": "Find shortest path from source to all nodes.",
                "problem_statement": "Given a weighted directed graph and source node, return shortest distances to all nodes.",
                "test_cases": [
                    {"input": "graph={0:[(1,4),(2,1)],1:[(3,1)],2:[(1,2),(3,5)],3:[]}, src=0", "expected_output": "{0:0,1:3,2:1,3:4}"},
                ],
            },
        ],
    },
    "trees": {
        "EASY": [
            {
                "title": "Binary Tree Inorder Traversal",
                "description": "Return the inorder traversal of a binary tree.",
                "problem_statement": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
                "test_cases": [
                    {"input": "[1,null,2,3]", "expected_output": "[1,3,2]"},
                ],
            },
        ],
        "MEDIUM": [
            {
                "title": "Validate Binary Search Tree",
                "description": "Determine if a binary tree is a valid BST.",
                "problem_statement": "Given root of a binary tree, return True if it is a valid binary search tree.",
                "test_cases": [
                    {"input": "[5,1,4,null,null,3,6]", "expected_output": "False"},
                    {"input": "[2,1,3]", "expected_output": "True"},
                ],
            },
        ],
        "HARD": [
            {
                "title": "Serialize and Deserialize Binary Tree",
                "description": "Design an algorithm to serialize/deserialize a binary tree.",
                "problem_statement": "Implement serialize(root) and deserialize(data) for a binary tree.",
                "test_cases": [
                    {"input": "[1,2,3,null,null,4,5]", "expected_output": "[1,2,3,null,null,4,5]"},
                ],
            },
        ],
    },
}


class CodingQuestionGenerator(QuestionGenerator):
    """Generates CodingQuestionEntity objects from hardcoded topic templates."""

    def generate(self, topic: str, difficulty: str, count: int) -> List[CodingQuestionEntity]:
        topic_lower = topic.lower()
        difficulty_upper = difficulty.upper()

        templates = (
            CODING_TEMPLATES.get(topic_lower, {}).get(difficulty_upper, [])
        )

        if not templates:
            # Fall back to EASY templates from the topic if exact difficulty unavailable
            templates = list(CODING_TEMPLATES.get(topic_lower, {}).values())
            templates = [t for sublist in templates for t in sublist]

        # Repeat or slice to hit exactly `count`
        if len(templates) == 0:
            return []
        
        result = []
        for i in range(count):
            tmpl = templates[i % len(templates)]
            result.append(
                CodingQuestionEntity(
                    id=str(uuid.uuid4()),
                    title=tmpl["title"],
                    description=tmpl["description"],
                    difficulty=difficulty_upper,
                    topic=topic_lower,
                    question_type=QuestionType.CODING.value,
                    problem_statement=tmpl["problem_statement"],
                    test_cases=tmpl.get("test_cases", []),
                    solution_code="",
                )
            )
        return result
