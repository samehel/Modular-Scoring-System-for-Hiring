// src/pages/public/ResumeSubmissionPage.tsx
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Alert,
  Box,
  Button,
  Card,
  Container,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { useResumeSubmissionViewModel } from '../../viewmodels/ResumeSubmissionViewModel';
import FileUpload from '../../components/shared/FileUpload';
import ResultDisplay from '../../components/candidate/ResultDisplay';

export default function ResumeSubmissionPage() {
  const { token } = useParams<{ token: string }>();
  const vm = useResumeSubmissionViewModel();

  // Reset when the token changes
  useEffect(() => {
    vm.reset();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  if (!token) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red" title="Invalid Link">
          This assessment link is missing a token. Please check the URL and try again.
        </Alert>
      </Container>
    );
  }

  return (
    <Box style={{ minHeight: '100vh', background: 'var(--mantine-color-gray-0)' }}>
      {/* Header */}
      <Box
        py="md"
        px="xl"
        style={{
          borderBottom: '1px solid var(--mantine-color-gray-3)',
          background: '#fff',
        }}
      >
        <Group justify="space-between">
          <Title order={3}>Resume Assessment</Title>
          <Text size="sm" c="dimmed" style={{ fontFamily: 'monospace' }}>
            Token: {token.slice(0, 8)}…
          </Text>
        </Group>
      </Box>

      <Container size="sm" py="xl">
        <Stack gap="xl">
          {vm.error && (
            <Alert
              color="red"
              title="Submission Error"
              withCloseButton
              onClose={vm.reset}
            >
              {vm.error}
            </Alert>
          )}

          {!vm.isSubmitted ? (
            <Card withBorder radius="md" p="lg">
              <Stack gap="lg">
                <Stack gap="xs">
                  <Title order={4}>Submit Your Resume</Title>
                  <Text c="dimmed" size="sm">
                    Upload your PDF resume below. Your submission will be automatically
                    scored against the assessment criteria.
                  </Text>
                </Stack>

                <FileUpload
                  file={vm.file}
                  onFileSelect={vm.uploadFile}
                  accept="application/pdf"
                  maxSizeMb={5}
                />

                <Group justify="flex-end">
                  <Button
                    id="submit-resume-btn"
                    size="md"
                    loading={vm.loading}
                    disabled={!vm.file}
                    onClick={() => vm.submitResume(token)}
                  >
                    {vm.loading ? 'Analyzing…' : 'Submit Resume'}
                  </Button>
                </Group>

                {vm.loading && (
                  <Group justify="center" gap="sm">
                    <Loader size="sm" />
                    <Text size="sm" c="dimmed">
                      Parsing and scoring your resume…
                    </Text>
                  </Group>
                )}
              </Stack>
            </Card>
          ) : (
            vm.result && (
              <Stack gap="md">
                <Alert color="green" title="Submission Successful">
                  Your resume has been received and scored. Here are your results:
                </Alert>
                <ResultDisplay result={vm.result} />
                <Button
                  id="submit-another-btn"
                  variant="light"
                  onClick={vm.reset}
                >
                  Submit Another Resume
                </Button>
              </Stack>
            )
          )}
        </Stack>
      </Container>
    </Box>
  );
}
