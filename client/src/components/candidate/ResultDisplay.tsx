// src/components/candidate/ResultDisplay.tsx
import { Badge, Card, Group, Progress, Stack, Table, Text, Title } from '@mantine/core';
import { ResumeSubmissionResult } from '../../services/submission.service';

interface Props {
  result: ResumeSubmissionResult;
}

export default function ResultDisplay({ result }: Props) {
  const { scores = [], parsed_data = {} } = result;
  
  // Re-calculate to avoid negative values from older DB records
  const maxPossible = scores.reduce((sum, s) => sum + (s?.max_score ?? 0), 0);
  const clampedTotalScore = scores.reduce((sum, s) => sum + Math.max(0, s?.score ?? 0), 0);
  const percentage = maxPossible > 0 ? Math.max(0, (clampedTotalScore / maxPossible) * 100) : 0;

  const getColor = (pct: number) => {
    if (pct >= 75) return 'green';
    if (pct >= 50) return 'yellow';
    return 'red';
  };

  return (
    <Stack gap="lg">
      {/* Overall score */}
      <Card withBorder radius="md" p="lg">
        <Stack gap="sm">
          <Group justify="space-between" align="center">
            <Title order={4}>Your Score</Title>
            <Badge size="xl" color={getColor(percentage)} variant="filled" radius="md">
              {clampedTotalScore.toFixed(1)} / {maxPossible.toFixed(1)}
            </Badge>
          </Group>
          <Progress
            value={percentage}
            color={getColor(percentage)}
            size="lg"
            radius="md"
          />
          <Text size="sm" c="dimmed" ta="right">{percentage.toFixed(1)}%</Text>
        </Stack>
      </Card>

      {/* Criterion breakdown */}
      {scores.length > 0 && (
        <Card withBorder radius="md" p="lg">
          <Title order={5} mb="md">Criterion Breakdown</Title>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Criterion</Table.Th>
                <Table.Th>Score</Table.Th>
                <Table.Th>Max</Table.Th>
                <Table.Th>Result</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {scores.map((s, i) => {
                const clampedScore = Math.max(0, s?.score ?? 0);
                const pct = s?.max_score > 0 ? (clampedScore / s.max_score) * 100 : 0;
                return (
                  <Table.Tr key={s?.criterion_id ?? i}>
                    <Table.Td>{s?.criterion_name ?? '-'}</Table.Td>
                    <Table.Td>{clampedScore.toFixed(1)}</Table.Td>
                    <Table.Td>{s?.max_score?.toFixed(1) ?? '-'}</Table.Td>
                    <Table.Td>
                      <Badge color={getColor(pct)} variant="light" size="sm">
                        {pct.toFixed(0)}%
                      </Badge>
                    </Table.Td>
                  </Table.Tr>
                );
              })}
            </Table.Tbody>
          </Table>
        </Card>
      )}

      {/* Parsed resume sections */}
      {Object.keys(parsed_data).length > 0 && (
        <Card withBorder radius="md" p="lg">
          <Title order={5} mb="md">Parsed Resume Sections</Title>
          <Stack gap="xs">
            {Object.entries(parsed_data)
              .filter(([, val]) => val)
              .map(([section, content]) => (
                <Stack key={section} gap={2}>
                  <Text fw={600} size="sm" tt="capitalize">{section}</Text>
                  <Text size="sm" c="dimmed" style={{ whiteSpace: 'pre-wrap' }}>
                    {content}
                  </Text>
                </Stack>
              ))}
          </Stack>
        </Card>
      )}
    </Stack>
  );
}
