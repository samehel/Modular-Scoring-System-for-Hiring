import { RegisterAdminDTO, RegisterCandidateDTO, LoginDTO, UserProfileDTO } from "../models/auth.types";
import api from "./api.service";

class AuthService {
    static async registerAdmin(data: RegisterAdminDTO): Promise<void> {
        await api.post(
            '/auth/register/admin/',
            data
        );
    }

    static async registerCandidate(data: RegisterCandidateDTO): Promise<void> {
        await api.post(
            '/auth/register/candidate/',
            data
        );
    }

    static async login(credentials: LoginDTO): Promise<void> {
        await api.post(
            '/auth/login/',
            credentials
        );
    }

    static async getProfile(): Promise<UserProfileDTO> {
        const res = await api.get('/auth/profile/')
        return res.data;
    }

    static async logout(): Promise<{ message: string }> {
        const res = await api.post('/auth/logout/');
        return res.data;
    }
}

export default AuthService;