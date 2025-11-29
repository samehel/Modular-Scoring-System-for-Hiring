// src/models/auth.types.ts
export interface RegisterAdminDTO {
    email: string;
    password: string;
    company_name: string;
    industry: string;
}

export interface RegisterCandidateDTO {
    email: string;
    password: string;
    phone: string;
    date_of_birth: string;
}

export interface LoginDTO {
    email: string;
    password: string;
}

export interface UserProfileDTO {
    user_id: string;
    email: string;
    user_type: string;
    profile_data: Record<string, any>;
    created_at: string;
}