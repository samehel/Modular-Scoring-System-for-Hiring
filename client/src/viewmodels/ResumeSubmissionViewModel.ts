// src/viewmodels/ResumeSubmissionViewModel.ts
import { useState, useCallback } from 'react';
import SubmissionService, { ResumeSubmissionResult } from '../services/submission.service';

const MAX_FILE_SIZE_MB = 5;
const ALLOWED_MIME = 'application/pdf';

export function useResumeSubmissionViewModel() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResumeSubmissionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);

  /** Validate and store the selected file. */
  const uploadFile = useCallback((selectedFile: File) => {
    setError(null);
    if (selectedFile.type !== ALLOWED_MIME) {
      setError('Only PDF files are accepted');
      return;
    }
    const sizeMb = selectedFile.size / (1024 * 1024);
    if (sizeMb > MAX_FILE_SIZE_MB) {
      setError(`File size must be under ${MAX_FILE_SIZE_MB} MB`);
      return;
    }
    setFile(selectedFile);
  }, []);

  /** Submit the stored file against the assessment token. */
  const submitResume = useCallback(
    async (token: string) => {
      if (!file) { setError('Please select a PDF file first'); return; }

      setLoading(true);
      setError(null);
      try {
        const data = await SubmissionService.submitResume(token, file);
        setResult(data);
        setIsSubmitted(true);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Submission failed');
      } finally {
        setLoading(false);
      }
    },
    [file],
  );

  const reset = useCallback(() => {
    setFile(null);
    setResult(null);
    setError(null);
    setLoading(false);
    setIsSubmitted(false);
  }, []);

  return { file, loading, result, error, isSubmitted, uploadFile, submitResume, reset };
}
