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
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { RegisterCandidateDTO } from '../../models/auth.types';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';

const CandidateRegisterPage = () => {
  const { registerCandidate } = useAuth();
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<RegisterCandidateDTO>({
    initialValues: {
      email: '',
      password: '',
      phone: '',
      date_of_birth: '',
    },
    validate: {
      email: (value: string) => (/^\S+@\S+$/.test(value) ? null : 'Enter a valid email'),
      password: (value: string) =>
        value.length >= 8 ? null : 'Password must contain at least 8 characters',
      phone: (value: string) =>
        /^\+?[0-9]{7,15}$/.test(value.trim()) ? null : 'Enter a valid phone number',
      date_of_birth: (value: string) => (value ? null : 'Select your date of birth'),
    },
  });

  const handleSubmit = form.onSubmit(async (values) => {
    setSubmitting(true);
    try {
      await registerCandidate(values);
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
              Build your candidate profile
            </Title>
            <Text c="dimmed">
              Create your account and track progress through every stage of evaluation. See exactly how your profile is being scored.
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
                  label="Email address"
                  placeholder="you@email.com"
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
                  label="Phone number"
                  placeholder="+1 555 000 1111"
                  type="tel"
                  inputMode="tel"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('phone')}
                />
                <TextInput
                  label="Date of birth"
                  type="date"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('date_of_birth')}
                />

                <Button
                  type="submit"
                  loading={submitting}
                  radius="md"
                  size="md"
                  fullWidth
                  mt="md"
                >
                  Create profile
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
                Setting up for your company?
              </Text>
              <Anchor
                component={Link}
                to="/admin-register"
                size="sm"
                style={{ color: '#5c47ff', textDecoration: 'none', fontWeight: 600 }}
              >
                Create admin workspace
              </Anchor>
            </Group>
          </Stack>
        </Stack>
      </Container>
    </Box>
  );
};

export default CandidateRegisterPage;
