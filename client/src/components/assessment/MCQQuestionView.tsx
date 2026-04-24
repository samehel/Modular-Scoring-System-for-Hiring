// src/components/assessment/MCQQuestionView.tsx
import { Radio, Stack, Text } from '@mantine/core';

interface Props {
  question: { title: string; description: string; choices: string[] };
  value: string;
  onChange: (val: string) => void;
}

export default function MCQQuestionView({ question, value, onChange }: Props) {
  return (
    <Stack gap="md">
      <Text fw={600} size="lg">{question.title}</Text>
      <Text c="dimmed">{question.description}</Text>
      <Radio.Group value={value} onChange={onChange} name="mcq-answer">
        <Stack gap="sm" mt="xs">
          {question.choices.map((choice, i) => (
            <Radio key={i} value={choice} label={choice} id={`choice-${i}`} />
          ))}
        </Stack>
      </Radio.Group>
    </Stack>
  );
}
