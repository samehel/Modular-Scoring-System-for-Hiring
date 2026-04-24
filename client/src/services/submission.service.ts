// src/services/submission.service.ts
import api from './api.service';
import { AssessmentResultDTO } from '../models/assessment.types';

export interface ResumeSubmissionResult {
  message: string;
  result_id?: string;
  total_score: number;
  scores: AssessmentResultDTO['score_breakdown'];
  parsed_data: Record<string, string>;
}

class SubmissionService {
  /**
   * Submit a PDF resume against a public assessment link.
   *
   * @param token   - The link token extracted from the URL
   * @param file    - PDF File object selected by the candidate
   */
  static async submitResume(
    token: string,
    file: File,
  ): Promise<ResumeSubmissionResult> {
    const formData = new FormData();
    formData.append('link_token', token);
    formData.append('resume', file);

    const res = await api.post('/api/public/submit/resume/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    return res.data as ResumeSubmissionResult;
  }
}

export default SubmissionService;
