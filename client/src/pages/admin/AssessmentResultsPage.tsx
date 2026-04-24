// src/pages/admin/AssessmentResultsPage.tsx
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Alert,
  Badge,
  Box,
  Button,
  Card,
  Container,
  Group,
  Loader,
  SimpleGrid,
  Stack,
  Table,
  Text,
  Title,
} from '@mantine/core';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import ResultService, { AssessmentStatistics } from '../../services/result.service';
import { AssessmentResultDTO } from '../../models/assessment.types';

export default function AssessmentResultsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [results, setResults] = useState<AssessmentResultDTO[]>([]);
  const [stats, setStats] = useState<AssessmentStatistics | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const limit = 10;

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [res, s] = await Promise.all([
          ResultService.getAssessmentResults(id, page, limit),
          ResultService.getStatistics(id),
        ]);
        setResults(res.results ?? []);
        setTotal(res.total ?? 0);
        setStats(s);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load results');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id, page]);

  const totalPages = Math.ceil(total / limit);

  // Build histogram buckets
  const buckets = [
    { range: '0–20', count: 0 },
    { range: '21–40', count: 0 },
    { range: '41–60', count: 0 },
    { range: '61–80', count: 0 },
    { range: '81–100', count: 0 },
  ];
  results.forEach((r) => {
    const s = r.total_score;
    if (s <= 20) buckets[0].count++;
    else if (s <= 40) buckets[1].count++;
    else if (s <= 60) buckets[2].count++;
    else if (s <= 80) buckets[3].count++;
    else buckets[4].count++;
  });

  return (
    <Box style={{ minHeight: '100vh', background: 'var(--mantine-color-gray-0)' }}>
      <Box
        style={{ borderBottom: '1px solid var(--mantine-color-gray-3)', background: '#fff' }}
        py="md" px="xl"
      >
        <Group justify="space-between">
          <Title order={3}>Assessment Results</Title>
          <Button variant="subtle" onClick={() => navigate('/admin/dashboard')}>← Dashboard</Button>
        </Group>
      </Box>

      <Container size="xl" py="xl">
        <Stack gap="xl">
          {error && <Alert color="red" title="Error">{error}</Alert>}

          {/* Stats Cards */}
          {stats && (
            <SimpleGrid cols={{ base: 2, md: 4 }} spacing="md">
              {[
                { label: 'Total Submissions', value: stats.submission_count, color: 'blue' },
                { label: 'Average Score', value: `${stats.avg_score}%`, color: 'teal' },
                { label: 'Passed', value: stats.pass_count, color: 'green' },
                { label: 'Failed', value: stats.fail_count, color: 'red' },
              ].map((stat) => (
                <Card key={stat.label} withBorder radius="md" p="lg">
                  <Text size="sm" c="dimmed">{stat.label}</Text>
                  <Text fw={700} size="xl" c={stat.color}>{stat.value}</Text>
                </Card>
              ))}
            </SimpleGrid>
          )}

          {/* Score Distribution */}
          {results.length > 0 && (
            <Card withBorder radius="md" p="lg">
              <Title order={5} mb="md">Score Distribution</Title>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={buckets}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="range" />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#339af0" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          )}

          {/* Results Table */}
          {loading ? (
            <Group justify="center"><Loader /></Group>
          ) : results.length === 0 ? (
            <Card withBorder radius="md" p="xl">
              <Text ta="center" c="dimmed">No submissions yet for this assessment.</Text>
            </Card>
          ) : (
            <Card withBorder radius="md" style={{ overflow: 'hidden' }}>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Candidate</Table.Th>
                    <Table.Th>Score</Table.Th>
                    <Table.Th>Result</Table.Th>
                    <Table.Th>Submitted</Table.Th>
                    <Table.Th />
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {results.map((r, i) => {
                    const passed = r.total_score >= 50;
                    return (
                      <Table.Tr key={r.id ?? i}>
                        <Table.Td>{r.candidate_id ?? 'Anonymous'}</Table.Td>
                        <Table.Td><Text fw={600}>{r.total_score.toFixed(1)}%</Text></Table.Td>
                        <Table.Td>
                          <Badge color={passed ? 'green' : 'red'} variant="light">
                            {passed ? 'Passed' : 'Failed'}
                          </Badge>
                        </Table.Td>
                        <Table.Td>
                          <Text size="sm" c="dimmed">
                            {new Date(r.submitted_at).toLocaleString()}
                          </Text>
                        </Table.Td>
                        <Table.Td>
                          {r.id && (
                            <Button
                              size="xs"
                              variant="subtle"
                              onClick={() => navigate(`/admin/results/${r.id}`)}
                            >
                              View
                            </Button>
                          )}
                        </Table.Td>
                      </Table.Tr>
                    );
                  })}
                </Table.Tbody>
              </Table>
            </Card>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <Group justify="center" gap="sm">
              <Button variant="subtle" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>← Prev</Button>
              <Text size="sm" c="dimmed">Page {page} of {totalPages}</Text>
              <Button variant="subtle" disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>Next →</Button>
            </Group>
          )}
        </Stack>
      </Container>
    </Box>
  );
}
