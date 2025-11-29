import { createContext, useContext, useEffect, useState } from "react";
import { LoginDTO, RegisterAdminDTO, RegisterCandidateDTO, UserProfileDTO } from "../models/auth.types"
import AuthService from "../services/auth.service";
import { toast } from "react-toastify";

type AuthContextType = {
    user: UserProfileDTO | null;
    loading: boolean;
    isAuthenticated: boolean;
    logout: () => Promise<void>;
    login: (credentials: LoginDTO) => Promise<void>;
    registerAdmin: (data: RegisterAdminDTO) => Promise<void>;
    registerCandidate: (data: RegisterCandidateDTO) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<UserProfileDTO | null>(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const logout = async () => {
        try {
            const res = await AuthService.logout();
            toast(res.message);
        } catch {
            toast('Failed to logout');
        }

        setUser(null);
        setIsAuthenticated(false);
        setLoading(false);
        window.location.replace('/');
    }

    const login = async (credentials: LoginDTO) => {
        try {
            await AuthService.login(credentials);
            const userProfile: UserProfileDTO = await AuthService.getProfile();
            setUser(userProfile);
            setIsAuthenticated(true);
            toast('Successfully logged in')
        } catch {
            toast('Failed to login')
        }
    }

    const registerAdmin = async (data: RegisterAdminDTO) => {
        try {
            await AuthService.registerAdmin(data);
            toast('Successfully Registered as Admin');
        } catch {
            toast('Failed to register as Admin')
        }
    }

    const registerCandidate = async (data: RegisterCandidateDTO) => {
        try {
            await AuthService.registerCandidate(data);
            toast('Successfully Registered as Candidate');
        } catch {
            toast('Failed to register as Candidate')
        }
    }
    
  useEffect(() => {
    let mounted = true;
    const init = async () => {
      try {
        const payload: UserProfileDTO = await AuthService.getProfile(); 
        if (payload) {
          if (!mounted) 
            return;
          setUser(payload);
          setIsAuthenticated(true);
        } else {
          setUser(null);
          setIsAuthenticated(false);
        }
      } catch {
        setUser(null);
        setIsAuthenticated(false);
      } finally {
        if (mounted) 
            setLoading(false);
      }
    };
    init();
    return () => {
      mounted = false;
    };
  }, []);

    return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, logout, login, registerAdmin, registerCandidate }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) 
    throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};