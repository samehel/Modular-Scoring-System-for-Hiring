import {
  Anchor,
  Box,
  Button,
  Card,
  Container,
  Divider,
  Group,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { Link } from 'react-router-dom';

const LandingPage = () => {
    return (
        <Box style={{ minHeight: '100vh', background: '#ffffff', color: '#1a1a1a' }}>
            {/* Navigation */}
            <Box
            style={{
                borderBottom: '1px solid #e5e5e5',
                background: '#fafafa',
            }}
            py="md"
            >
            <Container size="xl">
                <Group justify="space-between">
                <Title order={3} style={{ fontSize: '1.5rem', fontWeight: 700 }}>
                    Scoring Platform
                </Title>
                <Group gap="md">
                    <Anchor component={Link} to="/login" style={{ color: '#666', textDecoration: 'none' }}>
                    Sign in
                    </Anchor>
                    <Button component={Link} to="/admin-register" radius="md" size="md">
                    Get started
                    </Button>
                </Group>
                </Group>
            </Container>
            </Box>

            {/* Hero Section */}
            <Container size="xl" py={80}>
            <Stack gap={60} align="center" style={{ textAlign: 'center' }}>
                <Stack gap="md">
                <Title order={1} style={{ fontSize: '3.5rem', fontWeight: 800, lineHeight: 1.1 }}>
                    Build adaptive scoring models with confidence
                </Title>
                <Text size="lg" c="dimmed">
                    Design modular evaluation templates with weighted criteria, pass/fail rules, and optional bonuses. Score applicants consistently across HR teams, universities, and interviewers—without touching core code.
                </Text>
                <Group gap="md" justify="center" mt="lg">
                    <Button component={Link} to="/admin-register" size="lg" radius="md" py={8} px={32}>
                    Create workspace
                    </Button>
                    <Button
                    component={Link}
                    to="/candidate-register"
                    size="lg"
                    radius="md"
                    variant="light"
                    py={8}
                    px={32}
                    >
                    Apply as candidate
                    </Button>
                </Group>
                </Stack>
            </Stack>
            </Container>

            <Divider />

            {/* How It Works */}
            <Container size="xl" py={80}>
            <Stack gap={50}>
                <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
                <Title order={2} style={{ fontSize: '2.5rem', fontWeight: 700 }}>
                    Three steps to publish scoring templates
                </Title>
                <Text c="dimmed" size="lg" maw={600}>
                    Define criteria, configure rules, and deploy instantly to your entire hiring team.
                </Text>
                </Stack>

                <SimpleGrid cols={{ base: 1, md: 3 }} spacing={40}>
                {[
                    {
                    title: 'Define Weighted Criteria',
                    description: 'Set weighted components for resume quality, technical skills, interviews, background checks, and optional bonuses.',
                    },
                    {
                    title: 'Create Rule Objects',
                    description: 'Attach pass/fail gates, custom validators, and independent scoring strategies to each component.',
                    },
                    {
                    title: 'Deploy Models',
                    description: 'Publish completed templates to HR teams, universities, and interviewers without code changes.',
                    },
                ].map((step, idx) => (
                    <Card key={idx} padding="lg" radius="lg" withBorder style={{ borderColor: '#e5e5e5' }}>
                    <Stack gap="md">
                        <Box
                        style={{
                            width: 48,
                            height: 48,
                            borderRadius: 8,
                            background: '#f0f0ff',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 700,
                            color: '#5c47ff',
                            fontSize: '1.25rem',
                        }}
                        >
                        {idx + 1}
                        </Box>
                        <Stack gap="xs">
                        <Text fw={600} size="lg">
                            {step.title}
                        </Text>
                        <Text c="dimmed">{step.description}</Text>
                        </Stack>
                    </Stack>
                    </Card>
                ))}
                </SimpleGrid>
            </Stack>
            </Container>

            <Divider />

            {/* Use Cases */}
            <Container size="xl" py={80}>
            <Stack gap={50}>
                <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
                <Title order={2} style={{ fontSize: '2.5rem', fontWeight: 700 }}>
                    Built for every stakeholder
                </Title>
                </Stack>

                <SimpleGrid cols={{ base: 1, md: 3 }} spacing={30}>
                {[
                    {
                    title: 'Administrators',
                    description: 'Design reusable templates, monitor consistency, and iterate on models in real time.',
                    },
                    {
                    title: 'Interview Panels',
                    description: 'Score candidates using structured checklists with zero spreadsheet inconsistencies.',
                    },
                    {
                    title: 'Candidates',
                    description: 'Understand how each component contributes to your final evaluation and optimize accordingly.',
                    },
                ].map((persona, idx) => (
                    <Card key={idx} padding="lg" radius="lg" style={{ background: '#f9f9f9', border: '1px solid #e5e5e5' }}>
                    <Stack gap="md">
                        <Text fw={600} size="lg">
                        {persona.title}
                        </Text>
                        <Text c="dimmed" size="sm">
                        {persona.description}
                        </Text>
                    </Stack>
                    </Card>
                ))}
                </SimpleGrid>
            </Stack>
            </Container>

            <Divider />

            {/* Features */}
            <Container size="xl" py={80}>
            <Stack gap={50}>
                <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
                <Title order={2} style={{ fontSize: '2.5rem', fontWeight: 700 }}>
                    Composable scoring components
                </Title>
                <Text c="dimmed" size="lg" maw={600}>
                    Build scoring models with pluggable rule objects that work independently and can be tested separately.
                </Text>
                </Stack>

                <SimpleGrid cols={{ base: 1, md: 3 }} spacing={30}>
                {[
                    {
                    title: 'Resume Quality',
                    description: 'Weighted evaluation of resume components with customizable scoring rubrics.',
                    },
                    {
                    title: 'Coding Tests',
                    description: 'Integrate technical assessments with automatic pass/fail gates and bonus multipliers.',
                    },
                    {
                    title: 'Background Checks',
                    description: 'Independent compliance screening with policy gates and full audit trails.',
                    },
                ].map((feature, idx) => (
                    <Card key={idx} padding="lg" radius="lg" withBorder style={{ borderColor: '#e5e5e5' }}>
                    <Stack gap="md">
                        <Text fw={600} size="lg">
                        {feature.title}
                        </Text>
                        <Text c="dimmed">{feature.description}</Text>
                    </Stack>
                    </Card>
                ))}
                </SimpleGrid>
            </Stack>
            </Container>

            {/* CTA Footer */}
            <Box style={{ background: '#f9f9f9', borderTop: '1px solid #e5e5e5' }} py={80}>
            <Container size="xl">
                <Stack gap="md" align="center" style={{ textAlign: 'center' }}>
                <Title order={2} style={{ fontSize: '2rem', fontWeight: 700 }}>
                    Start building your scoring platform
                </Title>
                <Text c="dimmed">
                    Create a workspace to design custom evaluation templates and manage candidate scoring across your organization.
                </Text>
                <Group gap="md" justify="center" mt="md">
                    <Button component={Link} to="/admin-register" size="lg" radius="md">
                    Create admin workspace
                    </Button>
                    <Button component={Link} to="/login" size="lg" radius="md" variant="light">
                    Sign in
                    </Button>
                </Group>
                </Stack>
            </Container>
            </Box>
        </Box>
    );
};

export default LandingPage;
