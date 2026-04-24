// src/pages/candidate/CandidateHistoryPage.tsx
import { useEffect, useState } from 'react';
import {
  Alert,
  Badge,
  Box,
  Button,
  Card,
  Container,
  Group,
  Loader,
  Stack,
  Table,
  Text,
  Title,
} from '@mantine/core';
import AssessmentService from '../../services/assessment.service';
import { AssessmentResultDTO } from '../../models/assessment.types';
import { useAuth } from '../../contexts/AuthContext';

const TYPE_COLORS: Record<string, string> = {
  RESUME: 'blue',
  CODING: 'violet',
  INTERVIEW: 'teal',
};

export default function CandidateHistoryPage() {
  const { user, logout } = useAuth();
  const [results, setResults] = useState<AssessmentResultDTO[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const limit = 10;

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await AssessmentService.getCandidateHistory(page, limit);
        setResults(data.results ?? []);
        setTotal(data.total ?? 0);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load history');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [page]);

  const totalPages = Math.ceil(total / limit);

  return (
    <Box style={{ minHeight: '100vh', background: 'var(--mantine-color-gray-0)' }}>
      {/* Header */}
      <Box
        style={{ borderBottom: '1px solid var(--mantine-color-gray-3)', background: '#fff' }}
        py="md"
        px="xl"
      >
        <Group justify="space-between">
          <Stack gap={0}>
            <Title order={3}>My Assessment History</Title>
            <Text size="sm" c="dimmed">{user?.email}</Text>
          </Stack>
          <Button variant="subtle" id="logout-btn" onClick={logout}>
            Logout
          </Button>
        </Group>
      </Box>

      <Container size="xl" py="xl">
        <Stack gap="lg">
          {error && <Alert color="red" title="Error">{error}</Alert>}

          {loading ? (
            <Group justify="center" py="xl"><Loader /></Group>
          ) : results.length === 0 ? (
            <Card withBorder radius="md" p="xl">
              <Stack align="center" gap="md">
                <Text size="xl">📭</Text>
                <Title order={4}>No submissions yet</Title>
                <Text c="dimmed" ta="center">
                  You haven't submitted any assessments. Use a shared link to get started.
                </Text>
              </Stack>
            </Card>
          ) : (
            <Card withBorder radius="md" style={{ overflow: 'hidden' }}>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Assessment</Table.Th>
                    <Table.Th>Type</Table.Th>
                    <Table.Th>Score</Table.Th>
                    <Table.Th>Submitted</Table.Th>
                    <Table.Th>Status</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {results.map((r, i) => (
                    <Table.Tr key={r.id ?? i}>
                      <Table.Td>
                        <Text fw={500}>{r.assessment_name ?? r.assessment_id}</Text>
                      </Table.Td>
                      <Table.Td>
                        <Badge
                          color={TYPE_COLORS[r.assessment_type ?? ''] ?? 'gray'}
                          variant="light"
                        >
                          {r.assessment_type ?? '—'}
                        </Badge>
                      </Table.Td>
                      <Table.Td>
                        <Text fw={600}>{r.total_score.toFixed(1)}</Text>
                      </Table.Td>
                      <Table.Td>
                        <Text size="sm" c="dimmed">
                          {new Date(r.submitted_at).toLocaleString()}
                        </Text>
                      </Table.Td>
                      <Table.Td>
                        <Badge color="green" variant="dot">
                          Completed
                        </Badge>
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Card>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <Group justify="center" gap="sm">
              <Button
                variant="subtle"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
                id="prev-page-btn"
              >
                ← Previous
              </Button>
              <Text size="sm" c="dimmed">
                Page {page} of {totalPages}
              </Text>
              <Button
                variant="subtle"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                id="next-page-btn"
              >
                Next →
              </Button>
            </Group>
          )}
        </Stack>
      </Container>
    </Box>
  );
}
