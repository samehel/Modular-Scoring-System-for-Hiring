// src/pages/admin/ResultDetailPage.tsx
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Alert,
  Box,
  Button,
  Container,
  Group,
  Loader,
  Stack,
  Title,
} from '@mantine/core';
import ResultService from '../../services/result.service';
import { AssessmentResultDTO } from '../../models/assessment.types';
import ResultDisplay from '../../components/candidate/ResultDisplay';

export default function ResultDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [result, setResult] = useState<AssessmentResultDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await ResultService.getResultDetail(id);
        setResult(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load result details');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  return (
    <Box style={{ minHeight: '100vh', background: 'var(--mantine-color-gray-0)' }}>
      <Box
        style={{ borderBottom: '1px solid var(--mantine-color-gray-3)', background: '#fff' }}
        py="md" px="xl"
      >
        <Group justify="space-between">
          <Title order={3}>Result Details</Title>
          <Button variant="subtle" onClick={() => navigate(-1)}>← Back</Button>
        </Group>
      </Box>

      <Container size="md" py="xl">
        <Stack gap="xl">
          {error && <Alert color="red" title="Error">{error}</Alert>}

          {loading ? (
            <Group justify="center"><Loader /></Group>
          ) : result ? (
            <ResultDisplay result={result as any} />
          ) : null}
        </Stack>
      </Container>
    </Box>
  );
}
