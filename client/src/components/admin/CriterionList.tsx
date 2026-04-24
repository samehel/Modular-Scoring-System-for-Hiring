// src/components/admin/CriterionList.tsx
import { Badge, Group, Paper, Table, Text, Title } from '@mantine/core';
import { CriterionDTO } from '../../models/assessment.types';

interface Props {
  criteria: CriterionDTO[];
}

const TYPE_LABELS: Record<CriterionDTO['type'], string> = {
  KEYWORD_MATCH: 'Keyword Match',
  YEARS_EXPERIENCE: 'Years Experience',
  EDUCATION_LEVEL: 'Education Level',
  SKILLS_MATCH: 'Skills Match',
};

const TYPE_COLORS: Record<CriterionDTO['type'], string> = {
  KEYWORD_MATCH: 'blue',
  YEARS_EXPERIENCE: 'teal',
  EDUCATION_LEVEL: 'violet',
  SKILLS_MATCH: 'orange',
};

export default function CriterionList({ criteria }: Props) {
  if (criteria.length === 0) {
    return (
      <Paper withBorder p="md" radius="md">
        <Text c="dimmed" ta="center" py="lg">
          No criteria added yet. Add at least one criterion before generating a link.
        </Text>
      </Paper>
    );
  }

  const rows = criteria.map((c, i) => (
    <Table.Tr key={c.id ?? i}>
      <Table.Td>{c.name}</Table.Td>
      <Table.Td>
        <Badge color={TYPE_COLORS[c.type]} variant="light">
          {TYPE_LABELS[c.type]}
        </Badge>
      </Table.Td>
      <Table.Td>{(c.weight * 100).toFixed(0)}%</Table.Td>
      <Table.Td>
        <Text size="xs" c="dimmed" style={{ fontFamily: 'monospace' }}>
          {JSON.stringify(c.rules)}
        </Text>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Paper withBorder radius="md" style={{ overflow: 'hidden' }}>
      <Group px="md" py="sm">
        <Title order={5}>Scoring Criteria ({criteria.length})</Title>
      </Group>
      <Table striped highlightOnHover withTableBorder={false}>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>Type</Table.Th>
            <Table.Th>Weight</Table.Th>
            <Table.Th>Rules</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Paper>
  );
}
