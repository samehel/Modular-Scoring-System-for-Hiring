// src/models/assessment.types.ts

export interface CriterionDTO {
  id?: string;
  name: string;
  type: 'KEYWORD_MATCH' | 'YEARS_EXPERIENCE' | 'EDUCATION_LEVEL' | 'SKILLS_MATCH';
  weight: number; // 0–1 (e.g. 0.3 = 30%)
  rules: Record<string, unknown>;
}

export interface AssessmentDTO {
  id: string;
  name: string;
  description: string;
  type: 'RESUME' | 'CODING' | 'INTERVIEW';
  status: 'DRAFT' | 'ACTIVE' | 'CLOSED';
  criteria: CriterionDTO[];
  created_by: string;
  created_by_name?: string;
  created_at: string;
  updated_at: string;
}

export interface AssessmentLinkDTO {
  token: string;
  expiration: string;
}

export interface ScoreBreakdownDTO {
  criterion_id: string;
  criterion_name: string;
  score: number;
  max_score: number;
}

export interface AssessmentResultDTO {
  id?: string;
  assessment_id: string;
  assessment_name?: string;
  assessment_type?: string;
  total_score: number;
  submitted_at: string;
  parsed_data?: Record<string, string>;
  score_breakdown?: ScoreBreakdownDTO[];
  candidate_id?: string | null;
}

export interface CreateResumeAssessmentPayload {
  name: string;
  description: string;
}

export interface AddCriterionPayload {
  name: string;
  type: CriterionDTO['type'];
  weight: number;
  rules: Record<string, unknown>;
}
