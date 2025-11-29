import { ToastContainer } from 'react-toastify'
import { AuthProvider } from './contexts/AuthContext'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AdminRegisterPage from './pages/auth/AdminRegisterPage'
import CandidateRegisterPage from './pages/auth/CandidateRegisterPage'
import LandingPage from './pages/auth/LandingPage'
import LoginPage from './pages/auth/LoginPage'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/admin-register" element={<AdminRegisterPage />} />
          <Route path="/candidate-register" element={<CandidateRegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </BrowserRouter>
      <ToastContainer 
        theme="colored"
        position='bottom-right'
      />
    </AuthProvider>
  )
}

export default App
