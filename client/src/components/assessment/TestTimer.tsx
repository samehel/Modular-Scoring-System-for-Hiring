// src/components/assessment/TestTimer.tsx
import { useEffect } from 'react';
import { Badge, Group, Text } from '@mantine/core';

interface Props {
  timeRemaining: number;        // seconds
  formatted: string;            // "MM:SS"
  onExpire: () => void;
}

export default function TestTimer({ timeRemaining, formatted, onExpire }: Props) {
  useEffect(() => {
    if (timeRemaining === 0) onExpire();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeRemaining]);

  const isLow = timeRemaining <= 300; // ≤ 5 minutes

  return (
    <Group gap="xs" align="center">
      <Text size="sm" c="dimmed">Time remaining:</Text>
      <Badge
        id="test-timer"
        size="lg"
        color={isLow ? 'red' : 'blue'}
        variant={isLow ? 'filled' : 'light'}
        style={{ fontFamily: 'monospace', fontSize: '1rem' }}
      >
        {formatted}
      </Badge>
    </Group>
  );
}
