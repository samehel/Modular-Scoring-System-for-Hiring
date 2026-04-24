class ResumeResultDTO():
    def __init__(self, parsed_data: dict, scores: list, total_score: float, result_id: str = None) -> None:
        self.result_id = result_id
        self.parsed_data = parsed_data
        self.scores = scores
        self.total_score = total_score