from django.urls import path

# ── Admin — Resume Assessment ─────────────────────────────────────────────────
from assessments.presentation.views.admin.create_resume_assessment_view import CreateResumeAssessmentView
from assessments.presentation.views.admin.add_criterion_view import AddCriterionView
from assessments.presentation.views.admin.generate_link_view import GenerateLinkView
from assessments.presentation.views.admin.admin_assessment_list_view import AdminAssessmentListView

# ── Admin — Coding / Interview / Results (Phases 8, 12, 14) ──────────────────
from assessments.presentation.views.admin.assessment_management_views import (
    CreateCodingAssessmentView,
    CreateInterviewAssessmentView,
    AssessmentResultsView,
    ResultDetailView,
    AssessmentStatisticsView,
)

# ── Public — Resume Submission & Test Taking (Phases 4, 9) ───────────────────
from assessments.presentation.views.public.SubmitResumeView import SubmitResumeView
from assessments.presentation.views.public.TestViews import StartTestView, SubmitAnswerView, CompleteTestView

# ── Candidate — History (Phase 7) ────────────────────────────────────────────
from assessments.presentation.views.candidate.CandidateHistoryView import CandidateHistoryView

urlpatterns = [
    # Admin — Resume
    path("api/admin/assessments/resume/create/", CreateResumeAssessmentView.as_view(), name="create_resume_assessment"),
    path("api/admin/assessments/<str:id>/criteria/add/", AddCriterionView.as_view(), name="add_criterion"),
    path("api/admin/assessments/<str:id>/generate-link/", GenerateLinkView.as_view(), name="generate_link"),
    path("api/admin/assessments/", AdminAssessmentListView.as_view(), name="admin_assessments_list"),

    # Admin — Coding & Interview
    path("api/admin/assessments/coding/create/", CreateCodingAssessmentView.as_view(), name="create_coding_assessment"),
    path("api/admin/assessments/interview/create/", CreateInterviewAssessmentView.as_view(), name="create_interview_assessment"),

    # Admin — Results & Statistics
    path("api/admin/assessments/<str:assessment_id>/results/", AssessmentResultsView.as_view(), name="assessment_results"),
    path("api/admin/results/<str:result_id>/", ResultDetailView.as_view(), name="result_detail"),
    path("api/admin/assessments/<str:assessment_id>/statistics/", AssessmentStatisticsView.as_view(), name="assessment_statistics"),

    # Public — Resume Submission
    path("api/public/submit/resume/", SubmitResumeView.as_view(), name="submit_resume"),

    # Public — Test Taking
    path("api/public/test/start/", StartTestView.as_view(), name="start_test"),
    path("api/public/test/answer/", SubmitAnswerView.as_view(), name="submit_answer"),
    path("api/public/test/complete/", CompleteTestView.as_view(), name="complete_test"),

    # Candidate — History
    path("api/candidate/history/", CandidateHistoryView.as_view(), name="candidate_history"),
]