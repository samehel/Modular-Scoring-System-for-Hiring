// src/viewmodels/TestTakingViewModel.ts
import { useState, useCallback, useRef } from 'react';
import TestService, {
  CompleteTestResult,
  StartTestResult,
  TestQuestion,
} from '../services/test.service';

type TestStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';

export function useTestTakingViewModel() {
  const [session, setSession] = useState<StartTestResult | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [testStatus, setTestStatus] = useState<TestStatus>('NOT_STARTED');
  const [result, setResult] = useState<CompleteTestResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const startTimer = useCallback((minutes: number, onExpire: () => void) => {
    setTimeRemaining(minutes * 60);
    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current!);
          onExpire();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  }, []);

  const startTest = useCallback(async (token: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await TestService.startTest(token);
      setSession(data);
      setCurrentIndex(0);
      setAnswers({});
      setTestStatus('IN_PROGRESS');
      startTimer(data.time_limit, () => completeTest(data.session_id));
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to start test');
    } finally {
      setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [startTimer]);

  const currentQuestion: TestQuestion | null = session?.questions[currentIndex] ?? null;

  const nextQuestion = useCallback(() => {
    if (!session) return;
    setCurrentIndex((i) => Math.min(i + 1, session.questions.length - 1));
  }, [session]);

  const previousQuestion = useCallback(() => {
    setCurrentIndex((i) => Math.max(i - 1, 0));
  }, []);

  const saveAnswer = useCallback(async (answer: string) => {
    if (!session || !currentQuestion) return;
    setAnswers((prev) => ({ ...prev, [currentQuestion.id]: answer }));
    try {
      await TestService.submitAnswer(
        session.session_id,
        currentQuestion.id,
        currentQuestion.question_type,
        answer,
      );
    } catch {
      // Best-effort — errors don't block UX
    }
  }, [session, currentQuestion]);

  const completeTest = useCallback(async (overrideSessionId?: string) => {
    const sid = overrideSessionId ?? session?.session_id;
    if (!sid) return;
    if (timerRef.current) clearInterval(timerRef.current);
    setLoading(true);
    try {
      const data = await TestService.completeTest(sid);
      setResult(data);
      setTestStatus('COMPLETED');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to complete test');
    } finally {
      setLoading(false);
    }
  }, [session]);

  const formatTimeRemaining = useCallback(() => {
    const m = Math.floor(timeRemaining / 60).toString().padStart(2, '0');
    const s = (timeRemaining % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }, [timeRemaining]);

  return {
    session,
    currentIndex,
    currentQuestion,
    answers,
    timeRemaining,
    testStatus,
    result,
    loading,
    error,
    startTest,
    nextQuestion,
    previousQuestion,
    saveAnswer,
    completeTest,
    formatTimeRemaining,
  };
}
