// src/components/admin/CriterionForm.tsx
import { useState } from 'react';
import {
  ActionIcon,
  Badge,
  Button,
  Divider,
  Group,
  NumberInput,
  Paper,
  Select,
  Stack,
  Text,
  TextInput,
  Title,
  Tooltip,
} from '@mantine/core';
import { AddCriterionPayload, CriterionDTO } from '../../models/assessment.types';

interface Props {
  onAdd: (criterion: AddCriterionPayload) => void;
  loading: boolean;
}

const CRITERION_TYPES: { value: CriterionDTO['type']; label: string; description: string }[] = [
  {
    value: 'KEYWORD_MATCH',
    label: 'Keyword Match',
    description: 'Score based on how many specific keywords appear in the resume',
  },
  {
    value: 'YEARS_EXPERIENCE',
    label: 'Years of Experience',
    description: 'Score based on total years of professional experience',
  },
  {
    value: 'EDUCATION_LEVEL',
    label: 'Education Level',
    description: 'Score based on minimum required degree level',
  },
  {
    value: 'SKILLS_MATCH',
    label: 'Skills Match',
    description: 'Score based on required and optional technical skills',
  },
];

const EDUCATION_LEVELS = [
  { value: 'High School', label: '🏫 High School Diploma' },
  { value: 'Bachelors', label: '🎓 Bachelor\'s Degree' },
  { value: 'Masters', label: '📚 Master\'s Degree' },
  { value: 'Doctorate', label: '🔬 Doctorate' },
  { value: 'PhD', label: '🏅 PhD' },
];

// ── Tag input helper ─────────────────────────────────────────────────────────

function TagInput({
  label,
  description,
  placeholder,
  tags,
  onAdd,
  onRemove,
  color = 'blue',
}: {
  label: string;
  description?: string;
  placeholder: string;
  tags: string[];
  onAdd: (tag: string) => void;
  onRemove: (tag: string) => void;
  color?: string;
}) {
  const [draft, setDraft] = useState('');

  const commit = () => {
    const trimmed = draft.trim();
    if (trimmed && !tags.includes(trimmed)) {
      onAdd(trimmed);
    }
    setDraft('');
  };

  return (
    <Stack gap="xs">
      <div>
        <Text size="sm" fw={500}>{label}</Text>
        {description && <Text size="xs" c="dimmed">{description}</Text>}
      </div>

      <Group gap="xs" wrap="wrap">
        {tags.map((tag) => (
          <Badge
            key={tag}
            color={color}
            variant="light"
            size="md"
            rightSection={
              <Tooltip label="Remove">
                <ActionIcon
                  size="xs"
                  color={color}
                  variant="transparent"
                  onClick={() => onRemove(tag)}
                  aria-label={`Remove ${tag}`}
                >
                  ✕
                </ActionIcon>
              </Tooltip>
            }
          >
            {tag}
          </Badge>
        ))}
        {tags.length === 0 && (
          <Text size="xs" c="dimmed" fs="italic">No items yet — type below and press Enter or Add</Text>
        )}
      </Group>

      <Group gap="xs">
        <TextInput
          placeholder={placeholder}
          value={draft}
          onChange={(e) => setDraft(e.currentTarget.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); commit(); } }}
          style={{ flex: 1 }}
          size="sm"
        />
        <Button size="sm" variant="light" onClick={commit} disabled={!draft.trim()}>
          + Add
        </Button>
      </Group>
    </Stack>
  );
}

// ── Per-type rule forms ───────────────────────────────────────────────────────

function KeywordMatchRules({
  keywords,
  onChange,
}: {
  keywords: string[];
  onChange: (kw: string[]) => void;
}) {
  return (
    <TagInput
      label="Keywords"
      description="The resume will be scored for each keyword found in the text"
      placeholder="e.g. Python, REST, Agile…"
      tags={keywords}
      onAdd={(k) => onChange([...keywords, k])}
      onRemove={(k) => onChange(keywords.filter((x) => x !== k))}
      color="blue"
    />
  );
}

function YearsExperienceRules({
  minYears,
  maxYears,
  onChangeMin,
  onChangeMax,
}: {
  minYears: number;
  maxYears: number | null;
  onChangeMin: (v: number) => void;
  onChangeMax: (v: number | null) => void;
}) {
  return (
    <Stack gap="sm">
      <Text size="sm" fw={500}>Experience Range</Text>
      <Text size="xs" c="dimmed">
        Full score is awarded when the candidate's total experience falls within this range.
        Leave "Max years" empty for no upper limit.
      </Text>
      <Group grow>
        <NumberInput
          label="Min years"
          placeholder="e.g. 3"
          value={minYears}
          onChange={(v) => onChangeMin(Number(v))}
          min={0}
          max={50}
        />
        <NumberInput
          label="Max years (optional)"
          placeholder="No limit"
          value={maxYears ?? ''}
          onChange={(v) => onChangeMax(v === '' ? null : Number(v))}
          min={0}
          max={50}
          allowDecimal={false}
        />
      </Group>
    </Stack>
  );
}

function EducationLevelRules({
  minLevel,
  onChange,
}: {
  minLevel: string;
  onChange: (v: string) => void;
}) {
  return (
    <Stack gap="xs">
      <Text size="sm" fw={500}>Minimum Required Education Level</Text>
      <Text size="xs" c="dimmed">
        Full score if the candidate meets or exceeds this level. Partial score for one level below.
      </Text>
      <Select
        data={EDUCATION_LEVELS}
        value={minLevel}
        onChange={(v) => { if (v) onChange(v); }}
        allowDeselect={false}
      />
    </Stack>
  );
}

function SkillsMatchRules({
  required,
  optional,
  onChangeRequired,
  onChangeOptional,
}: {
  required: string[];
  optional: string[];
  onChangeRequired: (v: string[]) => void;
  onChangeOptional: (v: string[]) => void;
}) {
  return (
    <Stack gap="md">
      <TagInput
        label="Required Skills"
        description="Missing any of these skills will reduce the score significantly"
        placeholder="e.g. Python, PostgreSQL…"
        tags={required}
        onAdd={(s) => onChangeRequired([...required, s])}
        onRemove={(s) => onChangeRequired(required.filter((x) => x !== s))}
        color="red"
      />
      <Divider label="Optional Skills (bonus)" labelPosition="center" />
      <TagInput
        label="Optional / Nice-to-have Skills"
        description="Having these adds to the score but their absence doesn't penalize"
        placeholder="e.g. Docker, Kubernetes…"
        tags={optional}
        onAdd={(s) => onChangeOptional([...optional, s])}
        onRemove={(s) => onChangeOptional(optional.filter((x) => x !== s))}
        color="teal"
      />
    </Stack>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export default function CriterionForm({ onAdd, loading }: Props) {
  const [name, setName] = useState('');
  const [type, setType] = useState<CriterionDTO['type']>('KEYWORD_MATCH');
  const [weight, setWeight] = useState<number>(0.3);

  // Per-type rule state
  const [keywords, setKeywords] = useState<string[]>([]);
  const [minYears, setMinYears] = useState(2);
  const [maxYears, setMaxYears] = useState<number | null>(null);
  const [minLevel, setMinLevel] = useState('Bachelors');
  const [requiredSkills, setRequiredSkills] = useState<string[]>([]);
  const [optionalSkills, setOptionalSkills] = useState<string[]>([]);

  const buildRules = (): Record<string, unknown> => {
    switch (type) {
      case 'KEYWORD_MATCH':
        return { keywords };
      case 'YEARS_EXPERIENCE':
        return maxYears != null
          ? { min_years: minYears, max_years: maxYears }
          : { min_years: minYears };
      case 'EDUCATION_LEVEL':
        return { min_level: minLevel };
      case 'SKILLS_MATCH':
        return { required_skills: requiredSkills, optional_skills: optionalSkills };
    }
  };

  const isValid = (): boolean => {
    if (!name.trim()) return false;
    switch (type) {
      case 'KEYWORD_MATCH': return keywords.length > 0;
      case 'YEARS_EXPERIENCE': return minYears >= 0;
      case 'EDUCATION_LEVEL': return !!minLevel;
      case 'SKILLS_MATCH': return requiredSkills.length > 0;
    }
  };

  const handleSubmit = () => {
    if (!isValid()) return;
    onAdd({ name, type, weight, rules: buildRules() });
    // Reset all fields
    setName('');
    setWeight(0.3);
    setKeywords([]);
    setMinYears(2);
    setMaxYears(null);
    setMinLevel('Bachelors');
    setRequiredSkills([]);
    setOptionalSkills([]);
  };

  const selectedTypeMeta = CRITERION_TYPES.find((t) => t.value === type);

  return (
    <Paper withBorder p="md" radius="md">
      <Stack gap="md">
        <Title order={5}>Add Scoring Criterion</Title>

        {/* Name */}
        <TextInput
          id="criterion-name"
          label="Criterion Name"
          placeholder="e.g. Required Technical Skills"
          value={name}
          onChange={(e) => setName(e.currentTarget.value)}
          required
        />

        {/* Type */}
        <Select
          id="criterion-type"
          label="Criterion Type"
          data={CRITERION_TYPES.map(({ value, label }) => ({ value, label }))}
          value={type}
          onChange={(v) => { if (v) setType(v as CriterionDTO['type']); }}
          allowDeselect={false}
        />
        {selectedTypeMeta && (
          <Text size="xs" c="dimmed" mt={-8}>{selectedTypeMeta.description}</Text>
        )}

        {/* Weight */}
        <NumberInput
          id="criterion-weight"
          label="Weight"
          description="How much this criterion contributes to the total score (0 = 0%, 1 = 100%)"
          value={weight}
          onChange={(v) => setWeight(Number(v))}
          min={0}
          max={1}
          step={0.05}
          decimalScale={2}
          suffix=" of total"
        />

        <Divider label="Criterion Rules" labelPosition="left" />

        {/* Dynamic rule form */}
        {type === 'KEYWORD_MATCH' && (
          <KeywordMatchRules keywords={keywords} onChange={setKeywords} />
        )}
        {type === 'YEARS_EXPERIENCE' && (
          <YearsExperienceRules
            minYears={minYears}
            maxYears={maxYears}
            onChangeMin={setMinYears}
            onChangeMax={setMaxYears}
          />
        )}
        {type === 'EDUCATION_LEVEL' && (
          <EducationLevelRules minLevel={minLevel} onChange={setMinLevel} />
        )}
        {type === 'SKILLS_MATCH' && (
          <SkillsMatchRules
            required={requiredSkills}
            optional={optionalSkills}
            onChangeRequired={setRequiredSkills}
            onChangeOptional={setOptionalSkills}
          />
        )}

        <Group justify="flex-end" mt="xs">
          <Button
            id="add-criterion-btn"
            onClick={handleSubmit}
            loading={loading}
            disabled={!isValid()}
          >
            Add Criterion
          </Button>
        </Group>
      </Stack>
    </Paper>
  );
}
