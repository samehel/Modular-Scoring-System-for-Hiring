from datetime import date
import re

from assessments.domain.interfaces.scoring_strategy import ScoringStrategy
from assessments.domain.entities.criterion import Criterion
from assessments.domain.value_objects.criterion_type import CriterionType

class ResumeScoringStrategy(ScoringStrategy):
    
    def score(self, data: dict, criteria: list[Criterion]) -> float:

        # Exmaple input
        # {
        #     "education": "Harvard University\nBSc Computer Science, 2018–2022\n",
        #     "experience": "Software Engineer at X Corp, 2022–Present\n...",
        #     "skills": "Python, Django, React, AWS\n",
        #     "projects": "",
        #     "certifications": "",
        #     "summary": ""
        # }

        # Now we handle scoring of each criterion type on the resume
        total_weight = 0

        '''
        KEYWORD MATCH
        '''
        isKeywordMatchEnabled = any(criterion.type == CriterionType.KEYWORD_MATCH for criterion in criteria)
        if isKeywordMatchEnabled:
            criterion = next(criterion for criterion in criteria if criterion.type == CriterionType.KEYWORD_MATCH)

            if data["summary"] is None or data["summary"] == "":
                # We will assume that if the admin has this enabled, then they expect the candidate to have a summary
                # If they don't have the summary but the admin has this enabled, we will just deduct it completely from the candidate
                # Same logic will be applied to the rest of the matching algorithms
                total_weight -= (criterion.weight * 100)
            else:
                if "keywords" not in criterion.rules:
                    raise ValueError("There has to be at least one required keyword to search for")
                
                weight_key_word = (criterion.weight * 100) / len(criterion.rules["keywords"])

                for keyword in criterion.rules["keywords"]:
                    if keyword in data["summary"]:
                        total_weight += weight_key_word

        '''
        YEARS EXPERIENCE MATCH
        '''
        isYearsExperienceMatchEnabled = any(criterion.type == CriterionType.YEARS_EXPERIENCE for criterion in criteria)
        if isYearsExperienceMatchEnabled:
            criterion = next(criterion for criterion in criteria if criterion.type == CriterionType.YEARS_EXPERIENCE)

            if data["experience"] is None or data["experience"] == "":
                total_weight -= (criterion.weight * 100)
            else:
                if "min_years" not in criterion.rules:
                    raise ValueError("There has to be at least a min. years experience required")
                
                total_years_of_experience = 0
                pattern = r"(\d{4})\s*[-–]\s*(\d{4}|Present)"
                ranges = re.findall(pattern, data["experience"])

                for range in ranges:
                    if range[1].lower() != "present":
                        total_years_of_experience += int(range[1]) - int(range[0])
                    else:
                        total_years_of_experience += int(date.today().year) - int(range[0])

                if "max_years" not in criterion.rules:
                    if total_years_of_experience >= criterion.rules["min_years"]:
                        total_weight += (criterion.weight * 100)
                else:
                    if total_years_of_experience >= criterion.rules["min_years"] and total_years_of_experience <= criterion.rules["max_years"]:
                        total_weight += (criterion.weight * 100)

        '''
        EDUCATION LEVEL MATCH
        '''
        isEducationLevelMatchEnabled = any(criterion.type == CriterionType.EDUCATION_LEVEL for criterion in criteria)
        if isEducationLevelMatchEnabled:
            criterion = next(criterion for criterion in criteria if criterion.type == CriterionType.EDUCATION_LEVEL)

            if data["education"] is None or data["education"] == "":
                total_weight -= (criterion.weight * 100)
            else:
                if "min_level" not in criterion.rules:
                    raise ValueError("There has to be at least a min. level education required")

                if criterion.rules["min_level"] == "Bachelors":
                    pattern = r"\b(Bachelor'?s?|BSc|BS|BA|Master'?s?|MSc|MS|MA|Doctorate|Doctoral|PhD)\b"
                    isMinBachelors = re.search(pattern, data["education"], re.IGNORECASE)
                    if isMinBachelors:
                        total_weight += (criterion.weight * 100)
                elif criterion.rules["min_level"] == "Masters":
                    pattern = r"\b(Master'?s?|MSc|MS|MA|Doctorate|Doctoral|PhD)\b"
                    isMinMasters = re.search(pattern, data["education"], re.IGNORECASE)
                    if isMinMasters:
                        total_weight += (criterion.weight * 100)
                elif criterion.rules["min_level"] == "Doctorate":
                    pattern = r"\b(Doctorate|Doctoral)\b"
                    isMinDoctorate = re.search(pattern, data["education"], re.IGNORECASE)
                    if isMinDoctorate:
                        total_weight += (criterion.weight * 100)
                elif criterion.rules["min_level"] == "PhD":
                    pattern = r"\bPhD\b"
                    isMinPhD = re.search(pattern, data["education"], re.IGNORECASE)
                    if isMinPhD:
                        total_weight += (criterion.weight * 100)

        ''' 
        SKILLS MATCH
        '''
        isSkillMatchEnabled = any(criterion.type == CriterionType.SKILLS_MATCH for criterion in criteria)
        if isSkillMatchEnabled:
            criterion = next(criterion for criterion in criteria if criterion.type == CriterionType.SKILLS_MATCH)

            if data["skills"] is None or data["skills"] == "":
                total_weight -= (criterion.weight * 100)
            else:
                if "required_skills" not in criterion.rules:
                    raise ValueError("There has to be at least one required skill")
                
                # split the weight among the 
                total_skills_weight = criterion.weight * 100
                list_of_required_skills = criterion.rules["required_skills"]
                list_of_optional_skills = criterion.rules.get("optional_skills", [])
                candidate_skills = (data["skills"].replace("\n", ",")).split(",")

                if "optional_skills" not in criterion.rules:
                    # We get the total of required skills needed
                    # We get the percentage weight and split it among the skills
                    # For each skill they have from the required weight, they have their weight increased and vice versa
                    weight_per_skill = total_skills_weight / len(list_of_required_skills)

                    # Now we check if the candidate has the required skills
                    for skill in candidate_skills:
                        if skill.lower() in (required_skill.lower() for required_skill in list_of_required_skills):
                            total_weight += weight_per_skill
                else:
                    # If Optional skills are included, then we will add it to the mix
                    # However, required will be double the amount of weight optional will be
                    weight_per_skill = total_skills_weight / ((len(list_of_required_skills) * 2) + len(list_of_optional_skills))

                    weight_per_required_skill = weight_per_skill * 2
                    weight_per_optional_skill = weight_per_skill

                    for skill in candidate_skills:
                        if skill.lower() in (required_skill.lower() for required_skill in list_of_required_skills):
                            total_weight += weight_per_required_skill
                        elif skill.lower() in (optional_skill.lower() for optional_skill in list_of_optional_skills):
                            total_weight += weight_per_optional_skill

        return total_weight


        