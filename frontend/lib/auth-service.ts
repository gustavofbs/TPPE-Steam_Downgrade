// Serviço de autenticação para integração com o backend Django
import { fetchAPI } from './api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name?: string;
  last_name?: string;
}

export interface TokenResponse {
  token: string;
  user: {
    id: string;
    username: string;
    email: string;
  };
}

export interface UserProfile {
  bio?: string;
  birth_date?: string;
  avatar?: string;
}

// Classe de serviço de autenticação
export class AuthService {
  private static instance: AuthService;
  private tokenKey = 'authToken';
  private userKey = 'userData';

  private constructor() {}

  // Padrão Singleton para garantir uma única instância
  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  // Login do usuário
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    try {
      // Usando o endpoint de token do Django REST Framework
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Falha na autenticação');
      }

      const data = await response.json();
      
      // Armazenar token e dados do usuário
      this.setToken(data.token);
      this.setUserData(data.user);
      
      return data;
    } catch (error: any) {
      console.error('Erro de login:', error);
      throw new Error(error.message || 'Falha na autenticação');
    }
  }

  // Registro de novo usuário
  async register(userData: RegisterData): Promise<any> {
    try {
      const response = await fetchAPI('/users/', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
      
      return response;
    } catch (error: any) {
      console.error('Erro de registro:', error);
      throw new Error(error.message || 'Falha no registro');
    }
  }

  // Obter dados do usuário atual
  async getCurrentUser(): Promise<any> {
    try {
      const userData = await fetchAPI('/users/me/');
      this.setUserData(userData);
      return userData;
    } catch (error) {
      console.error('Erro ao obter dados do usuário:', error);
      throw error;
    }
  }

  // Atualizar perfil do usuário
  async updateProfile(userId: string, profileData: UserProfile): Promise<any> {
    try {
      return await fetchAPI(`/users/${userId}/update_profile/`, {
        method: 'PUT',
        body: JSON.stringify(profileData),
      });
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      throw error;
    }
  }

  // Alterar senha
  async changePassword(userId: string, passwordData: {
    old_password: string;
    new_password: string;
    new_password2: string;
  }): Promise<any> {
    try {
      return await fetchAPI(`/users/${userId}/change_password/`, {
        method: 'POST',
        body: JSON.stringify(passwordData),
      });
    } catch (error) {
      console.error('Erro ao alterar senha:', error);
      throw error;
    }
  }

  // Logout
  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
  }

  // Verificar se o usuário está autenticado
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Obter token
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.tokenKey);
    }
    return null;
  }

  // Definir token
  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.tokenKey, token);
    }
  }

  // Obter dados do usuário
  getUserData(): any {
    if (typeof window !== 'undefined') {
      const userData = localStorage.getItem(this.userKey);
      return userData ? JSON.parse(userData) : null;
    }
    return null;
  }

  // Definir dados do usuário
  private setUserData(userData: any): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.userKey, JSON.stringify(userData));
    }
  }
}
