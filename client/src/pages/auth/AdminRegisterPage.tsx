import { useState } from 'react';
import {
  Anchor,
  Box,
  Button,
  Card,
  Container,
  Group,
  Stack,
  Text,
  TextInput,
  Title,
  PasswordInput,
  Select,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { RegisterAdminDTO } from '../../models/auth.types';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';

const industries = [
  { value: 'Technology', label: 'Technology' },
  { value: 'Finance', label: 'Finance' },
  { value: 'Healthcare', label: 'Healthcare' },
  { value: 'Manufacturing', label: 'Manufacturing' },
  { value: 'Retail', label: 'Retail' },
  { value: 'Education', label: 'Education' },
  { value: 'Consulting', label: 'Consulting' },
  { value: 'Other', label: 'Other' },
];

const AdminRegisterPage = () => {
  const { registerAdmin } = useAuth();
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<RegisterAdminDTO>({
    initialValues: {
      email: '',
      password: '',
      company_name: '',
      industry: '',
    },
    validate: {
      email: (value: string) => (/^\S+@\S+$/.test(value) ? null : 'Enter a valid email'),
      password: (value: string) =>
        value.length >= 8 ? null : 'Password must contain at least 8 characters',
      company_name: (value: string) =>
        value.trim().length > 0 ? null : 'Company name is required',
      industry: (value: string) => (value ? null : 'Select an industry'),
    },
  });

  const handleSubmit = form.onSubmit(async (values) => {
    setSubmitting(true);
    try {
      await registerAdmin(values);
      form.reset();
    } finally {
      setSubmitting(false);
    }
  });

  return (
    <Box
      style={{
        minHeight: '100vh',
        background: '#ffffff',
        color: '#1a1a1a',
        display: 'flex',
        alignItems: 'center',
      }}
    >
      <Container size="sm" py={80}>
        <Stack gap={20} align="center">
          {/* Header */}
          <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
            <Title order={1} style={{ fontSize: '2rem', fontWeight: 700 }}>
              Create admin workspace
            </Title>
            <Text c="dimmed">
              Set up your scoring platform. Design templates, manage teams, and audit consistency across all evaluations.
            </Text>
          </Stack>

          {/* Back Link */}
          <Anchor
            component={Link}
            to="/"
            style={{
              color: '#5c47ff',
              textDecoration: 'none',
              fontSize: '0.875rem',
              fontWeight: 500,
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              alignSelf: 'flex-start',
            }}
          >
            ← Back to home
          </Anchor>

          {/* Form Card */}
          <Card
            padding="lg"
            radius="lg"
            withBorder
            style={{
              borderColor: '#e5e5e5',
              width: '100%',
              boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
            }}
          >
            <form onSubmit={handleSubmit}>
              <Stack gap="md">
                <TextInput
                  label="Work email"
                  placeholder="you@company.com"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('email')}
                />
                <PasswordInput
                  label="Password"
                  placeholder="At least 8 characters"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('password')}
                />
                <TextInput
                  label="Company name"
                  placeholder="Your company"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('company_name')}
                />
                <Select
                  label="Industry"
                  placeholder="Select your industry"
                  data={industries}
                  searchable
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('industry')}
                />

                <Button
                  type="submit"
                  loading={submitting}
                  radius="md"
                  size="md"
                  fullWidth
                  mt="md"
                >
                  Create workspace
                </Button>
              </Stack>
            </form>
          </Card>

          {/* Footer Links */}
          <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
            <Group gap="xs" justify="center">
              <Text size="sm" c="dimmed">
                Already have an account?
              </Text>
              <Anchor
                component={Link}
                to="/login"
                size="sm"
                style={{ color: '#5c47ff', textDecoration: 'none', fontWeight: 600 }}
              >
                Sign in
              </Anchor>
            </Group>
            <Group gap="xs" justify="center">
              <Text size="sm" c="dimmed">
                Looking to apply as a candidate?
              </Text>
              <Anchor
                component={Link}
                to="/candidate-register"
                size="sm"
                style={{ color: '#5c47ff', textDecoration: 'none', fontWeight: 600 }}
              >
                Register here
              </Anchor>
            </Group>
          </Stack>
        </Stack>
      </Container>
    </Box>
  );
};

export default AdminRegisterPage;
