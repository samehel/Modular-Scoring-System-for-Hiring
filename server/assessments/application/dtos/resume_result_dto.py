class ResumeResultDTO():
    def __init__(self, parsed_data: dict, scores: list, total_score: float) -> None:
        self.parsed_data = parsed_data
        self.scores = scores
        self.total_score = total_score