from assessments.domain.interfaces.result_repository import ResultRepository


class GetCandidateHistoryUseCase:
    """
    Returns all assessment results for a given candidate,
    sorted by submission date descending.
    """

    def __init__(self, result_repository: ResultRepository) -> None:
        self.result_repository = result_repository

    def execute(self, candidate_id: str) -> list:
        if not candidate_id:
            raise ValueError("candidate_id is required")

        results = self.result_repository.get_results_for_candidate(candidate_id)
        return results
