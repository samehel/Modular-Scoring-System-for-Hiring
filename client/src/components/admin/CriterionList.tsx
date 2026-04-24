// src/components/admin/CriterionList.tsx
import { ActionIcon, Badge, Group, Paper, Table, Text, Title, Tooltip } from '@mantine/core';
import { CriterionDTO } from '../../models/assessment.types';

interface Props {
  criteria: CriterionDTO[];
  onDelete?: (criterionId: string) => void;
  deleting?: boolean;
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

/** Renders criterion rules in a human-readable format — no raw JSON. */
function RulesSummary({ type, rules }: { type: CriterionDTO['type']; rules: Record<string, unknown> }) {
  switch (type) {
    case 'KEYWORD_MATCH': {
      const kw = (rules.keywords as string[] | undefined) ?? [];
      return (
        <Group gap={4} wrap="wrap">
          {kw.map((k) => (
            <Badge key={k} size="xs" variant="dot" color="blue">{k}</Badge>
          ))}
          {kw.length === 0 && <Text size="xs" c="dimmed">—</Text>}
        </Group>
      );
    }
    case 'YEARS_EXPERIENCE': {
      const min = rules.min_years as number;
      const max = rules.max_years as number | undefined;
      return (
        <Text size="xs" c="dimmed">
          {max != null ? `${min} – ${max} years` : `${min}+ years`}
        </Text>
      );
    }
    case 'EDUCATION_LEVEL': {
      return (
        <Text size="xs" c="dimmed">
          Min: {rules.min_level as string}
        </Text>
      );
    }
    case 'SKILLS_MATCH': {
      const req = (rules.required_skills as string[] | undefined) ?? [];
      const opt = (rules.optional_skills as string[] | undefined) ?? [];
      return (
        <Group gap={4} wrap="wrap">
          {req.map((s) => (
            <Badge key={s} size="xs" variant="dot" color="red">{s}</Badge>
          ))}
          {opt.map((s) => (
            <Badge key={s} size="xs" variant="dot" color="teal">{s}</Badge>
          ))}
          {req.length === 0 && opt.length === 0 && <Text size="xs" c="dimmed">—</Text>}
        </Group>
      );
    }
  }
}

export default function CriterionList({ criteria, onDelete, deleting }: Props) {
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
      <Table.Td fw={500}>{c.name}</Table.Td>
      <Table.Td>
        <Badge color={TYPE_COLORS[c.type]} variant="light">
          {TYPE_LABELS[c.type]}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Text size="sm" fw={600}>{(c.weight * 100).toFixed(0)}%</Text>
      </Table.Td>
      <Table.Td>
        <RulesSummary type={c.type} rules={c.rules} />
      </Table.Td>
      {onDelete && (
        <Table.Td>
          <Tooltip label="Delete criterion" position="left">
            <ActionIcon
              color="red"
              variant="subtle"
              size="sm"
              loading={deleting}
              onClick={() => c.id && onDelete(c.id)}
              aria-label={`Delete criterion ${c.name}`}
            >
              🗑
            </ActionIcon>
          </Tooltip>
        </Table.Td>
      )}
    </Table.Tr>
  ));

  return (
    <Paper withBorder radius="md" style={{ overflow: 'hidden' }}>
      <Group px="md" py="sm" justify="space-between">
        <Title order={5}>Scoring Criteria ({criteria.length})</Title>
        <Text size="xs" c="dimmed">
          <Badge color="red" size="xs" variant="dot" mr={4} />required skill &nbsp;
          <Badge color="teal" size="xs" variant="dot" mr={4} />optional skill
        </Text>
      </Group>
      <Table striped highlightOnHover withTableBorder={false}>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>Type</Table.Th>
            <Table.Th>Weight</Table.Th>
            <Table.Th>Rules</Table.Th>
            {onDelete && <Table.Th />}
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Paper>
  );
}
