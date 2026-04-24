import { ToastContainer } from 'react-toastify'
import { AuthProvider } from './contexts/AuthContext'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

// Auth pages (public)
import LandingPage from './pages/auth/LandingPage'
import LoginPage from './pages/auth/LoginPage'
import AdminRegisterPage from './pages/auth/AdminRegisterPage'
import CandidateRegisterPage from './pages/auth/CandidateRegisterPage'

// Admin pages (protected — ADMIN only)
import AdminDashboardPage from './pages/admin/AdminDashboardPage'
import CreateResumeAssessmentPage from './pages/admin/CreateResumeAssessmentPage'
import AssessmentResultsPage from './pages/admin/AssessmentResultsPage'

// Candidate pages (protected — CANDIDATE only)
import CandidateHistoryPage from './pages/candidate/CandidateHistoryPage'

// Public pages (no auth required)
import ResumeSubmissionPage from './pages/public/ResumeSubmissionPage'
import TakeTestPage from './pages/public/TakeTestPage'

// Route guard
import ProtectedRoute from './components/shared/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* ── Public ──────────────────────────────────────────── */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/admin-register" element={<AdminRegisterPage />} />
          <Route path="/candidate-register" element={<CandidateRegisterPage />} />

          {/* Public — resume submission */}
          <Route path="/assessment/:token" element={<ResumeSubmissionPage />} />
          {/* Public — coding / interview test */}
          <Route path="/assessment/test/:token" element={<TakeTestPage />} />

          {/* ── Admin (protected) ───────────────────────────────── */}
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute requiredUserType="ADMIN">
                <AdminDashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/assessments/resume/create"
            element={
              <ProtectedRoute requiredUserType="ADMIN">
                <CreateResumeAssessmentPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/assessments/:id/results"
            element={
              <ProtectedRoute requiredUserType="ADMIN">
                <AssessmentResultsPage />
              </ProtectedRoute>
            }
          />

          {/* ── Candidate (protected) ───────────────────────────── */}
          <Route
            path="/candidate/history"
            element={
              <ProtectedRoute requiredUserType="CANDIDATE">
                <CandidateHistoryPage />
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <ToastContainer theme="colored" position="bottom-right" />
    </AuthProvider>
  )
}

export default App
