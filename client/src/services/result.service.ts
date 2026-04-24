// src/services/result.service.ts
import api from './api.service';
import { AssessmentResultDTO } from '../models/assessment.types';

export interface AssessmentStatistics {
  submission_count: number;
  avg_score: number;
  min_score: number;
  max_score: number;
  pass_count: number;
  fail_count: number;
  pass_threshold: number;
}

class ResultService {
  static async getAssessmentResults(
    assessmentId: string,
    page = 1,
    limit = 10,
  ): Promise<{ total: number; page: number; results: AssessmentResultDTO[] }> {
    const res = await api.get(`/api/admin/assessments/${assessmentId}/results/`, {
      params: { page, limit },
    });
    return res.data;
  }

  static async getResultDetail(resultId: string): Promise<AssessmentResultDTO> {
    const res = await api.get(`/api/admin/results/${resultId}/`);
    return res.data as AssessmentResultDTO;
  }

  static async getStatistics(assessmentId: string): Promise<AssessmentStatistics> {
    const res = await api.get(`/api/admin/assessments/${assessmentId}/statistics/`);
    return res.data as AssessmentStatistics;
  }

  static async claimResult(resultId: string): Promise<void> {
    await api.post('/api/candidate/results/claim/', { result_id: resultId });
  }
}

export default ResultService;
