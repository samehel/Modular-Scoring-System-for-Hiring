// src/components/shared/FileUpload.tsx
import { useRef } from 'react';
import { Box, Button, Group, Stack, Text } from '@mantine/core';

interface Props {
  file: File | null;
  onFileSelect: (file: File) => void;
  accept?: string;
  maxSizeMb?: number;
}

export default function FileUpload({
  file,
  onFileSelect,
  accept = 'application/pdf',
  maxSizeMb = 5,
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];
    if (dropped) onFileSelect(dropped);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) onFileSelect(selected);
  };

  return (
    <Box
      id="file-upload-zone"
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      style={{
        border: '2px dashed var(--mantine-color-blue-4)',
        borderRadius: 12,
        padding: '2.5rem',
        textAlign: 'center',
        background: file ? 'var(--mantine-color-blue-0)' : 'var(--mantine-color-gray-0)',
        cursor: 'pointer',
        transition: 'background 0.2s',
      }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        style={{ display: 'none' }}
        onChange={handleChange}
        id="file-input"
      />
      <Stack gap="xs" align="center">
        <Text size="xl">📄</Text>
        {file ? (
          <>
            <Text fw={600} c="blue.7">{file.name}</Text>
            <Text size="sm" c="dimmed">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </Text>
          </>
        ) : (
          <>
            <Text fw={500}>Drag & drop your PDF here</Text>
            <Text size="sm" c="dimmed">or click to browse (max {maxSizeMb} MB)</Text>
          </>
        )}
        <Group justify="center" mt="sm">
          <Button
            id="browse-file-btn"
            variant="light"
            size="sm"
            onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
          >
            {file ? 'Replace file' : 'Browse file'}
          </Button>
        </Group>
      </Stack>
    </Box>
  );
}
