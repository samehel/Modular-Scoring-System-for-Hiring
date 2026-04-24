// src/components/admin/CriterionForm.tsx
import { useState } from 'react';
import {
  Button,
  Group,
  JsonInput,
  NumberInput,
  Select,
  Stack,
  Text,
  TextInput,
  Title,
  Paper,
} from '@mantine/core';
import { AddCriterionPayload, CriterionDTO } from '../../models/assessment.types';

interface Props {
  onAdd: (criterion: AddCriterionPayload) => void;
  loading: boolean;
}

const CRITERION_TYPES: { value: CriterionDTO['type']; label: string }[] = [
  { value: 'KEYWORD_MATCH', label: 'Keyword Match (summary section)' },
  { value: 'YEARS_EXPERIENCE', label: 'Years of Experience' },
  { value: 'EDUCATION_LEVEL', label: 'Education Level' },
  { value: 'SKILLS_MATCH', label: 'Skills Match' },
];

const RULES_PLACEHOLDERS: Record<CriterionDTO['type'], string> = {
  KEYWORD_MATCH: JSON.stringify({ keywords: ['Python', 'Django'] }, null, 2),
  YEARS_EXPERIENCE: JSON.stringify({ min_years: 3, max_years: 10 }, null, 2),
  EDUCATION_LEVEL: JSON.stringify({ min_level: 'Bachelors' }, null, 2),
  SKILLS_MATCH: JSON.stringify({ required_skills: ['Python'], optional_skills: ['Docker'] }, null, 2),
};

export default function CriterionForm({ onAdd, loading }: Props) {
  const [name, setName] = useState('');
  const [type, setType] = useState<CriterionDTO['type']>('KEYWORD_MATCH');
  const [weight, setWeight] = useState<number>(0.3);
  const [rulesJson, setRulesJson] = useState('{}');
  const [jsonError, setJsonError] = useState<string | null>(null);

  const handleSubmit = () => {
    setJsonError(null);
    let rules: Record<string, unknown>;
    try {
      rules = JSON.parse(rulesJson);
    } catch {
      setJsonError('Rules must be valid JSON');
      return;
    }
    onAdd({ name, type, weight, rules });
    // reset fields
    setName('');
    setWeight(0.3);
    setRulesJson('{}');
  };

  return (
    <Paper withBorder p="md" radius="md">
      <Stack gap="sm">
        <Title order={5}>Add Scoring Criterion</Title>

        <TextInput
          id="criterion-name"
          label="Criterion Name"
          placeholder="e.g. Required Skills"
          value={name}
          onChange={(e) => setName(e.currentTarget.value)}
          required
        />

        <Select
          id="criterion-type"
          label="Criterion Type"
          data={CRITERION_TYPES}
          value={type}
          onChange={(v) => {
            if (v) {
              setType(v as CriterionDTO['type']);
              setRulesJson(RULES_PLACEHOLDERS[v as CriterionDTO['type']]);
            }
          }}
        />

        <NumberInput
          id="criterion-weight"
          label="Weight (0 – 1)"
          description="Fraction of the total score this criterion contributes"
          value={weight}
          onChange={(v) => setWeight(Number(v))}
          min={0}
          max={1}
          step={0.05}
          decimalScale={2}
        />

        <JsonInput
          id="criterion-rules"
          label="Rules (JSON)"
          placeholder={RULES_PLACEHOLDERS[type]}
          value={rulesJson}
          onChange={setRulesJson}
          minRows={4}
          validationError="Invalid JSON"
          formatOnBlur
        />
        {jsonError && <Text c="red" size="sm">{jsonError}</Text>}

        <Group justify="flex-end">
          <Button
            id="add-criterion-btn"
            onClick={handleSubmit}
            loading={loading}
            disabled={!name.trim()}
          >
            Add Criterion
          </Button>
        </Group>
      </Stack>
    </Paper>
  );
}
