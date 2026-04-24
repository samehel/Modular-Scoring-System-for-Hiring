// src/components/shared/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';
import { Center, Loader } from '@mantine/core';
import { useAuth } from '../../contexts/AuthContext';

interface Props {
  children: React.ReactNode;
  /** If set, only users with this user_type may access the route. */
  requiredUserType?: 'ADMIN' | 'CANDIDATE';
}

/**
 * Wraps a route so that unauthenticated users are redirected to `/login`
 * and (optionally) users of the wrong type are redirected to `/`.
 */
export default function ProtectedRoute({ children, requiredUserType }: Props) {
  const { isAuthenticated, loading, user } = useAuth();

  // Wait for the auth context to finish initialising
  if (loading) {
    return (
      <Center style={{ height: '100vh' }}>
        <Loader />
      </Center>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requiredUserType && user?.user_type !== requiredUserType) {
    // Wrong role — redirect to the appropriate dashboard
    if (user?.user_type === 'ADMIN') return <Navigate to="/admin/dashboard" replace />;
    if (user?.user_type === 'CANDIDATE') return <Navigate to="/candidate/history" replace />;
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
