import { useState } from 'react';
import {
  Anchor,
  Box,
  Button,
  Card,
  Container,
  Group,
  PasswordInput,
  Stack,
  Text,
  TextInput,
  Title,
} from '@mantine/core';
import { useAuth } from '../../contexts/AuthContext';
import { LoginDTO } from '../../models/auth.types';
import { useForm } from '@mantine/form';
import { Link } from 'react-router-dom';

const LoginPage = () => {
  const { login } = useAuth();
  const [submitting, setSubmitting] = useState(false);
  const form = useForm<LoginDTO>({
    initialValues: {
      email: '',
      password: '',
    },
    validate: {
      email: (value: string) => (/^\S+@\S+$/.test(value) ? null : 'Enter a valid email'),
      password: (value: string) => (value ? null : 'Password is required'),
    },
  });

  const handleSubmit = form.onSubmit(async (values) => {
    setSubmitting(true);
    try {
      await login(values);
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
              Welcome back
            </Title>
            <Text c="dimmed">
              Sign in to access your scoring dashboard and manage evaluations.
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
                  placeholder="you@company.com"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('email')}
                />
                <PasswordInput
                  label="Password"
                  type="password"
                  placeholder="Enter your password"
                  size="md"
                  radius="md"
                  styles={{ input: { borderColor: '#e5e5e5' } }}
                  {...form.getInputProps('password')}
                />

                <Button
                  type="submit"
                  loading={submitting}
                  radius="md"
                  size="md"
                  fullWidth
                  mt="md"
                >
                  Sign in
                </Button>
              </Stack>
            </form>
          </Card>

          {/* Footer Links */}
          <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
            <Group gap="xs" justify="center">
              <Text size="sm" c="dimmed">
                Don't have an account?
              </Text>
              <Anchor
                component={Link}
                to="/candidate-register"
                size="sm"
                style={{ color: '#5c47ff', textDecoration: 'none', fontWeight: 600 }}
              >
                Sign up as candidate
              </Anchor>
            </Group>
            <Group gap="xs" justify="center">
              <Text size="sm" c="dimmed">
                Need an admin account?
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

export default LoginPage;
