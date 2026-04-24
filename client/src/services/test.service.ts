// src/services/test.service.ts
import api from './api.service';

export interface StartTestResult {
  session_id: string;
  assessment_id: string;
  assessment_name: string;
  questions: TestQuestion[];
  time_limit: number;
}

export interface TestQuestion {
  id: string;
  title: string;
  description: string;
  question_type: 'MCQ' | 'CODING' | 'TEXT';
  difficulty: string;
  topic: string;
  // MCQ
  choices?: string[];
  // Coding
  problem_statement?: string;
  // Interview
  category?: string;
}

export interface CompleteTestResult {
  result_id: string;
  session_id: string;
  total_score: number;
  answers: {
    question_id: string;
    score: number;
    is_correct: boolean | null;
    feedback: string;
  }[];
}

class TestService {
  static async startTest(token: string): Promise<StartTestResult> {
    const res = await api.post('/api/public/test/start/', { link_token: token });
    return res.data as StartTestResult;
  }

  static async submitAnswer(
    sessionId: string,
    questionId: string,
    questionType: string,
    answer: string,
  ): Promise<{ acknowledged: boolean }> {
    const res = await api.post('/api/public/test/answer/', {
      session_id: sessionId,
      question_id: questionId,
      question_type: questionType,
      answer_text: answer,
    });
    return res.data;
  }

  static async completeTest(sessionId: string): Promise<CompleteTestResult> {
    const res = await api.post('/api/public/test/complete/', { session_id: sessionId });
    return res.data as CompleteTestResult;
  }
}

export default TestService;
