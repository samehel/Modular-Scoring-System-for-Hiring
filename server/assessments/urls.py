from django.urls import path
from assessments.presentation.views.admin.create_resume_assessment_view import CreateResumeAssessmentView
from assessments.presentation.views.admin.add_criterion_view import AddCriterionView
from assessments.presentation.views.admin.generate_link_view import GenerateLinkView
from assessments.presentation.views.admin.admin_assessment_list_view import AdminAssessmentListView

urlpatterns = [
    path("admin/assessments/resume/create/", CreateResumeAssessmentView.as_view(), name="create_resume_assessment"),
    path("admin/assessments/<str:id>/criteria/add/", AddCriterionView.as_view(), name="add_criterion"),
    path("admin/assessments/<str:id>/generate-link/", GenerateLinkView.as_view(), name="generate_link"),
    path("admin/assessments/", AdminAssessmentListView.as_view(), name="admin_assessments_list"),
]