// src/viewmodels/ResumeAssessmentViewModel.ts
import { useState, useCallback } from 'react';
import AssessmentService from '../services/assessment.service';
import {
  AddCriterionPayload,
  AssessmentDTO,
  AssessmentLinkDTO,
  CriterionDTO,
} from '../models/assessment.types';

export function useResumeAssessmentViewModel() {
  const [assessment, setAssessment] = useState<AssessmentDTO | null>(null);
  const [criteria, setCriteria] = useState<CriterionDTO[]>([]);
  const [generatedLink, setGeneratedLink] = useState<AssessmentLinkDTO | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /** Create a new assessment — resets the ViewModel state. */
  const createAssessment = useCallback(
    async (name: string, description: string) => {
      if (!name.trim()) { setError('Assessment name is required'); return; }
      if (name.length > 255) { setError('Name must be 255 characters or less'); return; }
      if (!description.trim()) { setError('Description is required'); return; }

      setLoading(true);
      setError(null);
      try {
        const created = await AssessmentService.createResumeAssessment({ name, description });
        setAssessment(created);
        setCriteria(created.criteria ?? []);
        setGeneratedLink(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to create assessment');
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  /** Hydrate the ViewModel from an already-persisted AssessmentDTO (resume a draft). */
  const loadAssessment = useCallback((existing: AssessmentDTO) => {
    setAssessment(existing);
    setCriteria(existing.criteria ?? []);
    setGeneratedLink(null);
    setError(null);
  }, []);

  /** Add a criterion to the current assessment (persists to backend). */
  const addCriterion = useCallback(
    async (criterion: AddCriterionPayload) => {
      if (!assessment) { setError('Create an assessment first'); return; }
      if (!criterion.name.trim()) { setError('Criterion name is required'); return; }
      if (criterion.weight < 0 || criterion.weight > 1) {
        setError('Weight must be between 0 and 1');
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const updated = await AssessmentService.addCriterion(assessment.id, criterion);
        setAssessment(updated);
        setCriteria(updated.criteria ?? []);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to add criterion');
      } finally {
        setLoading(false);
      }
    },
    [assessment],
  );

  /** Delete a criterion by ID (persists to backend). */
  const deleteCriterion = useCallback(
    async (criterionId: string) => {
      if (!assessment) return;
      setLoading(true);
      setError(null);
      try {
        const remaining = await AssessmentService.deleteCriterion(assessment.id, criterionId);
        setCriteria(remaining);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to delete criterion');
      } finally {
        setLoading(false);
      }
    },
    [assessment],
  );

  /** Generate and store the shareable assessment link. */
  const generateLink = useCallback(async () => {
    if (!assessment) { setError('Create an assessment first'); return; }
    if (criteria.length === 0) {
      setError('Add at least one criterion before generating a link');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const link = await AssessmentService.generateLink(assessment.id);
      setGeneratedLink(link);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate link');
    } finally {
      setLoading(false);
    }
  }, [assessment, criteria]);

  /** Reset the entire ViewModel back to initial state. */
  const reset = useCallback(() => {
    setAssessment(null);
    setCriteria([]);
    setGeneratedLink(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    assessment,
    criteria,
    generatedLink,
    loading,
    error,
    createAssessment,
    loadAssessment,
    addCriterion,
    deleteCriterion,
    generateLink,
    reset,
  };
}
