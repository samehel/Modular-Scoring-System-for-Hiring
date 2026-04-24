// src/pages/admin/CreateResumeAssessmentPage.tsx
import { useEffect } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  Container,
  CopyButton,
  Divider,
  Group,
  Loader,
  Stack,
  Text,
  Textarea,
  TextInput,
  Title,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { useNavigate } from 'react-router-dom';
import { useResumeAssessmentViewModel } from '../../viewmodels/ResumeAssessmentViewModel';
import CriterionForm from '../../components/admin/CriterionForm';
import CriterionList from '../../components/admin/CriterionList';

export default function CreateResumeAssessmentPage() {
  const navigate = useNavigate();
  const vm = useResumeAssessmentViewModel();

  const form = useForm({
    initialValues: { name: '', description: '' },
    validate: {
      name: (v) => (!v.trim() ? 'Name is required' : v.length > 255 ? 'Max 255 characters' : null),
      description: (v) => (!v.trim() ? 'Description is required' : null),
    },
  });

  // Auto-clear errors after 5 seconds
  useEffect(() => {
    if (!vm.error) return;
    const t = setTimeout(() => {}, 5000);
    return () => clearTimeout(t);
  }, [vm.error]);

  const handleCreate = form.onSubmit(({ name, description }) => {
    vm.createAssessment(name, description);
  });

  const assessmentLink = vm.generatedLink
    ? `${window.location.origin}/assessment/${vm.generatedLink.token}`
    : null;

  return (
    <Box style={{ minHeight: '100vh', background: 'var(--mantine-color-gray-0)' }}>
      <Box
        style={{
          borderBottom: '1px solid var(--mantine-color-gray-3)',
          background: '#fff',
        }}
        py="md"
        px="xl"
      >
        <Group justify="space-between">
          <Title order={3}>Create Resume Assessment</Title>
          <Button variant="subtle" onClick={() => navigate('/admin/dashboard')}>
            ← Back to Dashboard
          </Button>
        </Group>
      </Box>

      <Container size="lg" py="xl">
        <Stack gap="xl">
          {vm.error && (
            <Alert color="red" title="Error" withCloseButton onClose={() => {}}>
              {vm.error}
            </Alert>
          )}

          {/* Step 1: Assessment info */}
          <Card withBorder radius="md" p="lg">
            <Stack gap="md">
              <Title order={4}>1. Assessment Details</Title>
              <form onSubmit={handleCreate}>
                <Stack gap="sm">
                  <TextInput
                    id="assessment-name"
                    label="Assessment Name"
                    placeholder="e.g. Senior Backend Engineer – Q3 2026"
                    required
                    {...form.getInputProps('name')}
                    disabled={!!vm.assessment}
                  />
                  <Textarea
                    id="assessment-description"
                    label="Description"
                    placeholder="Describe the role, requirements, and what this assessment measures."
                    rows={3}
                    required
                    {...form.getInputProps('description')}
                    disabled={!!vm.assessment}
                  />
                  {!vm.assessment && (
                    <Group justify="flex-end">
                      <Button
                        id="create-assessment-btn"
                        type="submit"
                        loading={vm.loading}
                      >
                        Create Assessment
                      </Button>
                    </Group>
                  )}
                  {vm.assessment && (
                    <Text size="sm" c="teal.7" fw={500}>
                      ✓ Assessment "{vm.assessment.name}" created (ID: {vm.assessment.id})
                    </Text>
                  )}
                </Stack>
              </form>
            </Stack>
          </Card>

          {/* Step 2: Criteria */}
          {vm.assessment && (
            <Stack gap="md">
              <Title order={4}>2. Scoring Criteria</Title>
              <CriterionForm onAdd={vm.addCriterion} loading={vm.loading} />
              <CriterionList criteria={vm.criteria} />
            </Stack>
          )}

          {/* Step 3: Generate Link */}
          {vm.assessment && (
            <>
              <Divider />
              <Card withBorder radius="md" p="lg">
                <Stack gap="md">
                  <Title order={4}>3. Generate Assessment Link</Title>
                  <Text c="dimmed" size="sm">
                    Once you generate a link, candidates can submit their resumes through it.
                    You need at least one criterion.
                  </Text>
                  {vm.loading && <Loader size="sm" />}
                  {!vm.generatedLink ? (
                    <Button
                      id="generate-link-btn"
                      onClick={vm.generateLink}
                      loading={vm.loading}
                      disabled={vm.criteria.length === 0}
                    >
                      Generate Link
                    </Button>
                  ) : (
                    <Stack gap="sm">
                      <Text fw={600} c="green.7">✓ Link generated successfully!</Text>
                      <Box
                        style={{
                          background: 'var(--mantine-color-gray-1)',
                          borderRadius: 8,
                          padding: '0.75rem 1rem',
                          fontFamily: 'monospace',
                          fontSize: '0.875rem',
                          wordBreak: 'break-all',
                        }}
                      >
                        {assessmentLink}
                      </Box>
                      <Group gap="sm">
                        <CopyButton value={assessmentLink!}>
                          {({ copied, copy }) => (
                            <Button
                              id="copy-link-btn"
                              variant={copied ? 'filled' : 'light'}
                              color={copied ? 'green' : 'blue'}
                              onClick={copy}
                            >
                              {copied ? '✓ Copied!' : 'Copy Link'}
                            </Button>
                          )}
                        </CopyButton>
                        <Text size="sm" c="dimmed">
                          Expires: {new Date(vm.generatedLink.expiration).toLocaleString()}
                        </Text>
                      </Group>
                    </Stack>
                  )}
                </Stack>
              </Card>
            </>
          )}
        </Stack>
      </Container>
    </Box>
  );
}
