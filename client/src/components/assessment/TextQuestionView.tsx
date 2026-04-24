// src/components/assessment/TextQuestionView.tsx
import { Badge, Stack, Text, Textarea } from '@mantine/core';

interface Props {
  question: { title: string; description: string; category?: string };
  value: string;
  onChange: (val: string) => void;
}

export default function TextQuestionView({ question, value, onChange }: Props) {
  return (
    <Stack gap="md">
      {question.category && (
        <Badge variant="light" color="teal" size="sm">{question.category}</Badge>
      )}
      <Text fw={600} size="lg">{question.title}</Text>
      <Text c="dimmed">{question.description}</Text>
      <Textarea
        id="text-answer"
        placeholder="Type your answer here…"
        value={value}
        onChange={(e) => onChange(e.currentTarget.value)}
        minRows={6}
        autosize
      />
    </Stack>
  );
}
