"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthService, LoginCredentials, RegisterData } from './auth-service';

// Define user type
export type User = {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile?: {
    bio: string;
    birth_date: string;
    avatar: string;
  };
};

// Define auth context type
type AuthContextType = {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: {
    username: string;
    email: string;
    password: string;
    password2: string;
    first_name?: string;
    last_name?: string;
  }) => Promise<void>;
  logout: () => void;
  updateProfile: (profileData: any) => Promise<void>;
};

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // Instância do serviço de autenticação
  const authService = AuthService.getInstance();

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (!authService.isAuthenticated()) {
        setIsLoading(false);
        return;
      }
      
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Authentication error:', error);
        authService.logout();
      } finally {
        setIsLoading(false);
      }
    };
    
    checkAuth();
  }, []);

  // Login function
  const login = async (username: string, password: string) => {
    setIsLoading(true);
    
    try {
      const credentials: LoginCredentials = { username, password };
      await authService.login(credentials);
      const userData = await authService.getCurrentUser();
      setUser(userData);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Register function
  const register = async (userData: RegisterData) => {
    setIsLoading(true);
    
    try {
      await authService.register(userData);
      // Auto login after registration
      await login(userData.username, userData.password);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  // Update profile function
  const updateProfile = async (profileData: any) => {
    if (!user) return;
    
    try {
      await authService.updateProfile(user.id, profileData);
      // Refresh user data
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        login,
        register,
        logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}
