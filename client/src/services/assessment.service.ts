// src/services/assessment.service.ts
import api from './api.service';
import {
  AddCriterionPayload,
  AssessmentDTO,
  AssessmentLinkDTO,
  AssessmentResultDTO,
  CreateResumeAssessmentPayload,
} from '../models/assessment.types';

class AssessmentService {
  // ── Admin ──────────────────────────────────────────────────────────────

  /** Create a new resume assessment (admin only). */
  static async createResumeAssessment(
    payload: CreateResumeAssessmentPayload,
  ): Promise<AssessmentDTO> {
    const res = await api.post('/api/admin/assessments/resume/create/', payload);
    return res.data.assessment as AssessmentDTO;
  }

  /** Add a scoring criterion to an existing assessment. */
  static async addCriterion(
    assessmentId: string,
    criterion: AddCriterionPayload,
  ): Promise<AssessmentDTO> {
    const res = await api.post(
      `/api/admin/assessments/${assessmentId}/criteria/add/`,
      criterion,
    );
    return res.data.assessment as AssessmentDTO;
  }

  /** Generate a shareable public link for an assessment. */
  static async generateLink(assessmentId: string): Promise<AssessmentLinkDTO> {
    const res = await api.post(
      `/api/admin/assessments/${assessmentId}/generate-link/`,
    );
    return res.data.link as AssessmentLinkDTO;
  }

  /** Fetch all assessments created by the logged-in admin. */
  static async getAdminAssessments(): Promise<AssessmentDTO[]> {
    const res = await api.get('/api/admin/assessments/');
    return res.data.assessments_list as AssessmentDTO[];
  }

  // ── Candidate ──────────────────────────────────────────────────────────

  /** Fetch paginated history for the logged-in candidate. */
  static async getCandidateHistory(
    page = 1,
    limit = 10,
  ): Promise<{ total: number; page: number; results: AssessmentResultDTO[] }> {
    const res = await api.get('/api/candidate/history/', {
      params: { page, limit },
    });
    return res.data;
  }
}

export default AssessmentService;
