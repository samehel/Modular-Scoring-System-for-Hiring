// src/pages/admin/AdminDashboardPage.tsx
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
  SimpleGrid,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import AssessmentService from '../../services/assessment.service';
import { AssessmentDTO } from '../../models/assessment.types';
import { useAuth } from '../../contexts/AuthContext';

const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'gray',
  ACTIVE: 'green',
  CLOSED: 'red',
};

export default function AdminDashboardPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [assessments, setAssessments] = useState<AssessmentDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await AssessmentService.getAdminAssessments();
        setAssessments(data ?? []);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load assessments');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

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
            <Title order={3}>Admin Dashboard</Title>
            <Text size="sm" c="dimmed">Welcome, {user?.email}</Text>
          </Stack>
          <Group gap="sm">
            <Button
              id="create-resume-assessment-btn"
              onClick={() => navigate('/admin/assessments/resume/create')}
            >
              + New Assessment
            </Button>
            <Button variant="subtle" onClick={logout} id="logout-btn">
              Logout
            </Button>
          </Group>
        </Group>
      </Box>

      <Container size="xl" py="xl">
        <Stack gap="xl">
          {error && (
            <Alert color="red" title="Error">
              {error}
            </Alert>
          )}

          {loading ? (
            <Group justify="center" py="xl">
              <Loader />
            </Group>
          ) : assessments.length === 0 ? (
            <Card withBorder radius="md" p="xl">
              <Stack align="center" gap="md">
                <Text size="xl">📋</Text>
                <Title order={4}>No assessments yet</Title>
                <Text c="dimmed" ta="center">
                  Create your first assessment to start evaluating candidates.
                </Text>
                <Button
                  id="create-first-assessment-btn"
                  onClick={() => navigate('/admin/assessments/resume/create')}
                >
                  Create Assessment
                </Button>
              </Stack>
            </Card>
          ) : (
            <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
              {assessments.map((a) => (
                <Card
                  key={a.id}
                  withBorder
                  radius="md"
                  p="lg"
                  style={{ cursor: 'pointer' }}
                  onClick={() => navigate(`/admin/assessments/${a.id}/results`)}
                >
                  <Stack gap="sm">
                    <Group justify="space-between" align="flex-start">
                      <Text fw={600} size="md" style={{ flex: 1 }}>
                        {a.name}
                      </Text>
                      <Badge color={STATUS_COLORS[a.status] ?? 'gray'} variant="light">
                        {a.status}
                      </Badge>
                    </Group>
                    <Text size="sm" c="dimmed" lineClamp={2}>
                      {a.description}
                    </Text>
                    <Group gap="xs">
                      <Badge variant="outline" size="sm">{a.type}</Badge>
                      <Text size="xs" c="dimmed">
                        {a.criteria?.length ?? 0} criteria
                      </Text>
                    </Group>
                    <Text size="xs" c="dimmed">
                      Created {new Date(a.created_at).toLocaleDateString()}
                    </Text>
                  </Stack>
                </Card>
              ))}
            </SimpleGrid>
          )}
        </Stack>
      </Container>
    </Box>
  );
}
