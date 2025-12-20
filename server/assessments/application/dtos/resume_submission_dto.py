from typing import Optional

class ResumeSubmissionDTO():
    def __init__(self, link_token: str, file: bytes, candidate_id: Optional[str]) -> None:
        self.link_token = link_token
        self.file = file
        self.candidate_id = candidate_id