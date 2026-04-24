// src/components/assessment/CodingQuestionView.tsx
import { lazy, Suspense } from 'react';
import { Badge, Card, Loader, Select, Stack, Text } from '@mantine/core';
import { useState } from 'react';

const MonacoEditor = lazy(() => import('@monaco-editor/react'));

const LANGUAGE_TEMPLATES: Record<string, string> = {
  python: '# Write your Python solution here\ndef solution():\n    pass\n',
  javascript: '// Write your JavaScript solution here\nfunction solution() {\n  \n}\n',
  java: '// Write your Java solution here\npublic class Solution {\n    public static void main(String[] args) {\n        // your code\n    }\n}\n',
  cpp: '// Write your C++ solution here\n#include <iostream>\nusing namespace std;\n\nint main() {\n    // your code\n    return 0;\n}\n',
};

interface Props {
  question: { title: string; description: string; problem_statement: string };
  value: string;
  onChange: (code: string) => void;
}

export default function CodingQuestionView({ question, value, onChange }: Props) {
  const [language, setLanguage] = useState('python');

  const handleLanguageChange = (lang: string | null) => {
    if (!lang) return;
    setLanguage(lang);
    if (!value || Object.values(LANGUAGE_TEMPLATES).includes(value)) {
      onChange(LANGUAGE_TEMPLATES[lang] ?? '');
    }
  };

  return (
    <Stack gap="md">
      <Text fw={600} size="lg">{question.title}</Text>
      <Card withBorder radius="md" p="md" style={{ background: 'var(--mantine-color-gray-0)' }}>
        <Text size="sm" style={{ whiteSpace: 'pre-wrap' }}>{question.problem_statement}</Text>
      </Card>

      <Select
        id="language-selector"
        label="Language"
        value={language}
        onChange={handleLanguageChange}
        data={[
          { value: 'python', label: 'Python' },
          { value: 'javascript', label: 'JavaScript' },
          { value: 'java', label: 'Java' },
          { value: 'cpp', label: 'C++' },
        ]}
        w={200}
      />

      <Badge variant="light" size="sm" color="orange">Code Editor</Badge>

      <Suspense fallback={<Loader size="sm" />}>
        <div style={{ border: '1px solid var(--mantine-color-gray-3)', borderRadius: 8, overflow: 'hidden' }}>
          <MonacoEditor
            height="350px"
            language={language === 'cpp' ? 'cpp' : language}
            value={value || LANGUAGE_TEMPLATES[language]}
            onChange={(v) => onChange(v ?? '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              wordWrap: 'on',
            }}
          />
        </div>
      </Suspense>
    </Stack>
  );
}
