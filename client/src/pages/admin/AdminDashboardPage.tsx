import { useEffect, useState } from 'react';
import {
  Alert,
  Badge,
  Box,
  Button,
  Card,
  Container,
  CopyButton,
  ActionIcon,
  Group,
  Loader,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { useLocation, useNavigate } from 'react-router-dom';
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
  const location = useLocation();
  const { user, logout } = useAuth();
  const [assessments, setAssessments] = useState<AssessmentDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Re-fetch every time this page is navigated to (location.key changes on each visit)
  useEffect(() => {
    setLoading(true);
    setError(null);
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
  }, [location.key]);


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
                >
                  <Stack gap="sm" style={{ height: '100%' }}>
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

                    {/* Action buttons */}
                    {a.status === 'ACTIVE' && a.link_token && (
                      <Group gap="xs" mt="sm">
                        <Text size="xs" fw={500}>Public Link:</Text>
                        <Group gap={4} wrap="nowrap" style={{ flex: 1, background: 'var(--mantine-color-gray-1)', padding: '4px 8px', borderRadius: '4px' }}>
                          <Text size="xs" style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
                            {`${window.location.origin}/assessment/${a.link_token}`}
                          </Text>
                          <CopyButton value={`${window.location.origin}/assessment/${a.link_token}`} timeout={2000}>
                            {({ copied, copy }) => (
                              <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
                                {copied ? '✓' : '📋'}
                              </ActionIcon>
                            )}
                          </CopyButton>
                        </Group>
                      </Group>
                    )}
                    
                    <Group gap="xs" mt="auto" pt="sm" style={{ borderTop: '1px solid var(--mantine-color-gray-2)' }}>
                      {a.status === 'DRAFT' && (
                        <Button
                          size="xs"
                          variant="light"
                          color="blue"
                          onClick={() =>
                            navigate('/admin/assessments/resume/create', {
                              state: { assessment: a },
                            })
                          }
                        >
                          ✏️ Continue Editing
                        </Button>
                      )}
                      <Button
                        size="xs"
                        variant="subtle"
                        onClick={() => navigate(`/admin/assessments/${a.id}/results`)}
                      >
                        📊 View Results
                      </Button>
                    </Group>
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
