"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from './api';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined: string;
  is_active: boolean;
  profile: {
    bio: string;
    birth_date: string | null;
    avatar: string | null;
  };
}

interface UserContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  refreshUser: () => Promise<void>;
  updateUser: (userData: Partial<User>) => Promise<void>;
  updateProfile: (profileData: any) => Promise<void>;
  uploadAvatar: (file: File) => Promise<User>;
  changePassword: (passwordData: { old_password: string; new_password: string; new_password2: string }) => Promise<void>;
}

const defaultContextValue: UserContextType = {
  user: null,
  isLoading: false,
  error: null,
  refreshUser: async () => {},
  updateUser: async () => {},
  updateProfile: async () => {},
  uploadAvatar: async () => ({ 
    id: 0, 
    username: '', 
    email: '', 
    first_name: '', 
    last_name: '', 
    date_joined: '', 
    is_active: true, 
    profile: { bio: '', birth_date: null, avatar: null } 
  }),
  changePassword: async () => {},
};

const UserContext = createContext<UserContextType>(defaultContextValue);

export function useUser() {
  const context = useContext(UserContext);
  return context;
}

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshUser = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (err: any) {
      console.error('Erro ao buscar dados do usuário:', err);
      setError(err.message || 'Erro ao carregar dados do usuário');
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = async (userData: Partial<User>) => {
    if (!user) throw new Error('Usuário não está logado');
    
    try {
      setError(null);
      const updatedUser = await authAPI.updateProfile(user.id.toString(), userData);
      setUser({ ...user, ...updatedUser });
    } catch (err: any) {
      console.error('Erro ao atualizar usuário:', err);
      setError(err.message || 'Erro ao atualizar dados do usuário');
      throw err;
    }
  };

  const updateProfile = async (profileData: any) => {
    if (!user) throw new Error('Usuário não está logado');
    
    try {
      setError(null);
      
      // Preparar dados para envio
      const updateData: any = {};
      
      // Adicionar dados básicos do usuário
      if (profileData.first_name) updateData.first_name = profileData.first_name;
      if (profileData.last_name) updateData.last_name = profileData.last_name;
      if (profileData.email) updateData.email = profileData.email;
      
      // Preparar dados do perfil (excluindo avatar que tem endpoint próprio)
      if (profileData.profile) {
        if (profileData.profile.bio !== undefined) updateData.bio = profileData.profile.bio;
        if (profileData.profile.birth_date) updateData.birth_date = profileData.profile.birth_date;
        // Avatar não é enviado aqui, tem endpoint próprio (uploadAvatar)
      }



      // Usar a API helper que já existe
      const updatedUser = await authAPI.updateProfile(user.id.toString(), updateData);
      
      // Atualizar o estado do usuário
      setUser(updatedUser);
      
    } catch (err: any) {
      console.error('Erro ao atualizar perfil:', err);
      setError(err.message || 'Erro ao atualizar perfil');
      throw err;
    }
  };

  const changePassword = async (passwordData: { old_password: string; new_password: string; new_password2: string }) => {
    if (!user) throw new Error('Usuário não está logado');
    
    try {
      setError(null);
      await authAPI.changePassword(user.id.toString(), passwordData);
    } catch (err: any) {
      console.error('Erro ao alterar senha:', err);
      setError(err.message || 'Erro ao alterar senha');
      throw err;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      refreshUser();
    } else {
      setIsLoading(false);
    }
  }, []);

  // Função para upload de avatar
  const uploadAvatar = async (file: File) => {
    if (!user) {
      throw new Error('Usuário não autenticado');
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('avatar', file);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/${user.id}/upload_avatar/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao fazer upload do avatar');
      }

      const userData = await response.json();
      setUser(userData);
      return userData;
    } catch (err: any) {
      setError(err.message || 'Erro ao fazer upload do avatar');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    user,
    isLoading,
    error,
    refreshUser,
    updateUser,
    updateProfile,
    uploadAvatar,
    changePassword,
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}
