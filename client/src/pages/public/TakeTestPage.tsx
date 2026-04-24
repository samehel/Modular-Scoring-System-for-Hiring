// src/pages/public/TakeTestPage.tsx
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Alert,
  Badge,
  Box,
  Button,
  Card,
  Container,
  Divider,
  Group,
  Loader,
  Progress,
  Stack,
  Table,
  Text,
  Title,
} from '@mantine/core';
import { useTestTakingViewModel } from '../../viewmodels/TestTakingViewModel';
import TestTimer from '../../components/assessment/TestTimer';
import QuestionNavigation from '../../components/assessment/QuestionNavigation';
import MCQQuestionView from '../../components/assessment/MCQQuestionView';
import CodingQuestionView from '../../components/assessment/CodingQuestionView';
import TextQuestionView from '../../components/assessment/TextQuestionView';

export default function TakeTestPage() {
  const { token } = useParams<{ token: string }>();
  const vm = useTestTakingViewModel();

  // Auto-start the test when the page loads
  useEffect(() => {
    if (token && vm.testStatus === 'NOT_STARTED') {
      vm.startTest(token);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  if (!token) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red" title="Invalid link">Missing assessment token in URL.</Alert>
      </Container>
    );
  }

  // Loading / start
  if (vm.loading && vm.testStatus === 'NOT_STARTED') {
    return (
      <Container size="sm" py="xl">
        <Group justify="center" py="xl" gap="md">
          <Loader />
          <Text>Loading assessment…</Text>
        </Group>
      </Container>
    );
  }

  // ── Completed ──
  if (vm.testStatus === 'COMPLETED' && vm.result) {
    const { total_score, answers } = vm.result;
    const passed = total_score >= 50;

    return (
      <Container size="md" py="xl">
        <Stack gap="xl">
          <Alert
            color={passed ? 'green' : 'orange'}
            title={passed ? '✓ Test Completed — Passed!' : 'Test Completed'}
          >
            Your total score: <strong>{total_score.toFixed(1)}%</strong>
          </Alert>

          <Card withBorder radius="md" p="lg">
            <Title order={5} mb="md">Answer Breakdown</Title>
            <Table striped>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>#</Table.Th>
                  <Table.Th>Score</Table.Th>
                  <Table.Th>Correct</Table.Th>
                  <Table.Th>Feedback</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {answers.map((a, i) => (
                  <Table.Tr key={a.question_id}>
                    <Table.Td>{i + 1}</Table.Td>
                    <Table.Td>{a.score.toFixed(0)}%</Table.Td>
                    <Table.Td>
                      <Badge color={a.is_correct ? 'green' : 'red'} variant="light" size="sm">
                        {a.is_correct === null ? 'Review' : a.is_correct ? 'Yes' : 'No'}
                      </Badge>
                    </Table.Td>
                    <Table.Td>
                      <Text size="xs" c="dimmed">{a.feedback}</Text>
                    </Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </Card>
        </Stack>
      </Container>
    );
  }

  // ── In Progress ──
  if (vm.testStatus === 'IN_PROGRESS' && vm.session && vm.currentQuestion) {
    const q = vm.currentQuestion;
    const total = vm.session.questions.length;
    const progress = ((vm.currentIndex + 1) / total) * 100;
    const currentAnswer = vm.answers[q.id] ?? '';

    return (
      <Box style={{ minHeight: '100vh', background: 'var(--mantine-color-gray-0)' }}>
        {/* Header */}
        <Box
          py="sm"
          px="xl"
          style={{
            borderBottom: '1px solid var(--mantine-color-gray-3)',
            background: '#fff',
            position: 'sticky',
            top: 0,
            zIndex: 100,
          }}
        >
          <Group justify="space-between">
            <Text fw={600}>{vm.session.assessment_name}</Text>
            <TestTimer
              timeRemaining={vm.timeRemaining}
              formatted={vm.formatTimeRemaining()}
              onExpire={() => vm.completeTest()}
            />
          </Group>
          <Progress value={progress} size="xs" mt="xs" color="blue" />
        </Box>

        <Container size="md" py="xl">
          <Stack gap="lg">
            {vm.error && <Alert color="red" title="Error">{vm.error}</Alert>}

            <Card withBorder radius="md" p="lg">
              {q.question_type === 'MCQ' && (
                <MCQQuestionView
                  question={q as Required<typeof q>}
                  value={currentAnswer}
                  onChange={(v) => vm.saveAnswer(v)}
                />
              )}
              {q.question_type === 'CODING' && (
                <CodingQuestionView
                  question={q as Required<typeof q>}
                  value={currentAnswer}
                  onChange={(v) => vm.saveAnswer(v)}
                />
              )}
              {q.question_type === 'TEXT' && (
                <TextQuestionView
                  question={q}
                  value={currentAnswer}
                  onChange={(v) => vm.saveAnswer(v)}
                />
              )}
            </Card>

            <Divider />

            <QuestionNavigation
              current={vm.currentIndex}
              total={total}
              onPrev={vm.previousQuestion}
              onNext={vm.nextQuestion}
              onComplete={() => vm.completeTest()}
              loading={vm.loading}
            />
          </Stack>
        </Container>
      </Box>
    );
  }

  // Error state
  if (vm.error) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red" title="Error">{vm.error}</Alert>
        <Button mt="md" onClick={() => window.location.reload()}>Retry</Button>
      </Container>
    );
  }

  return (
    <Container size="sm" py="xl">
      <Group justify="center"><Loader /></Group>
    </Container>
  );
}
