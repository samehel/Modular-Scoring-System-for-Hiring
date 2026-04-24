// src/components/assessment/QuestionNavigation.tsx
import { Button, Group, Text } from '@mantine/core';

interface Props {
  current: number;       // 0-indexed
  total: number;
  onPrev: () => void;
  onNext: () => void;
  onComplete: () => void;
  loading: boolean;
}

export default function QuestionNavigation({ current, total, onPrev, onNext, onComplete, loading }: Props) {
  const isFirst = current === 0;
  const isLast = current === total - 1;

  return (
    <Group justify="space-between" mt="md">
      <Button
        id="prev-question-btn"
        variant="subtle"
        disabled={isFirst}
        onClick={onPrev}
      >
        ← Previous
      </Button>

      <Text size="sm" c="dimmed">
        Question {current + 1} of {total}
      </Text>

      {isLast ? (
        <Button
          id="complete-test-btn"
          color="green"
          loading={loading}
          onClick={onComplete}
        >
          Submit Test
        </Button>
      ) : (
        <Button
          id="next-question-btn"
          onClick={onNext}
        >
          Next →
        </Button>
      )}
    </Group>
  );
}
