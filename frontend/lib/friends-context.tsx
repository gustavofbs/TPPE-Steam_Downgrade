"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { FriendsAPI, Friend, Friendship, FriendRequest, UserActivity, GameRecommendation } from './friends-api';
import { useAuth } from './auth-context';

interface FriendsContextType {
  // Estado dos dados
  friends: Friend[];
  onlineFriends: Friend[];
  pendingRequests: FriendRequest[];
  activities: UserActivity[];
  recommendations: GameRecommendation[];
  
  // Estados de carregamento
  isLoading: boolean;
  isLoadingFriends: boolean;
  isLoadingActivities: boolean;
  
  // Erros
  error: string | null;
  
  // Ações
  refreshFriends: () => Promise<void>;
  refreshActivities: () => Promise<void>;
  sendFriendRequest: (receiverId: string) => Promise<void>;
  acceptFriendRequest: (friendshipId: string) => Promise<void>;
  rejectFriendRequest: (friendshipId: string) => Promise<void>;
  removeFriend: (friendshipId: string) => Promise<void>;
  sendRecommendation: (receiverId: string, gameId: string, message: string) => Promise<void>;
  markRecommendationAsRead: (recommendationId: string) => Promise<void>;
  searchUsers: (query: string) => Promise<Friend[]>;
  
  // Utilitários
  getFriendshipStatus: (userId: string) => Promise<string | null>;
  isFriend: (userId: string) => boolean;
}

const FriendsContext = createContext<FriendsContextType | undefined>(undefined);

interface FriendsProviderProps {
  children: ReactNode;
}

export function FriendsProvider({ children }: FriendsProviderProps) {
  const { user, isAuthenticated } = useAuth();
  
  // Estados dos dados
  const [friends, setFriends] = useState<Friend[]>([]);
  const [onlineFriends, setOnlineFriends] = useState<Friend[]>([]);
  const [pendingRequests, setPendingRequests] = useState<FriendRequest[]>([]);
  const [activities, setActivities] = useState<UserActivity[]>([]);
  const [recommendations, setRecommendations] = useState<GameRecommendation[]>([]);
  
  // Estados de carregamento
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingFriends, setIsLoadingFriends] = useState(false);
  const [isLoadingActivities, setIsLoadingActivities] = useState(false);
  
  // Erros
  const [error, setError] = useState<string | null>(null);

  // ===== FUNÇÕES DE CARREGAMENTO =====

  const refreshFriends = async () => {
    if (!isAuthenticated || !user) return;
    
    setIsLoadingFriends(true);
    setError(null);
    
    try {
      // Carregar amigos
      const friendsData = await FriendsAPI.getFriends();
      const filteredFriends = friendsData.filter(friend => friend.id !== user.id);
      setFriends(filteredFriends);
      
      // Carregar amigos online
      const onlineFriendsData = await FriendsAPI.getOnlineFriends();
      const filteredOnlineFriends = onlineFriendsData.filter(friend => friend.id !== user.id);
      setOnlineFriends(filteredOnlineFriends);
      
      // Carregar solicitações pendentes
      const pendingData = await FriendsAPI.getPendingRequests();
      setPendingRequests(pendingData);
      
      // Carregar recomendações
      const recommendationsData = await FriendsAPI.getReceivedRecommendations();
      setRecommendations(recommendationsData);
      
    } catch (err: any) {
      console.error('Erro ao carregar dados de amigos:', err);
      setError(err.message || 'Erro ao carregar amigos');
    } finally {
      setIsLoadingFriends(false);
    }
  };

  const refreshActivities = async () => {
    if (!isAuthenticated) return;
    
    setIsLoadingActivities(true);
    
    try {
      const activitiesData = await FriendsAPI.getFriendsActivities();
      setActivities(activitiesData);
    } catch (err: any) {
      console.error('Erro ao carregar atividades:', err);
      setError(err.message || 'Erro ao carregar atividades');
    } finally {
      setIsLoadingActivities(false);
    }
  };

  // ===== AÇÕES DE AMIZADE =====

  const sendFriendRequest = async (receiverId: string) => {
    try {
      await FriendsAPI.sendFriendRequest(receiverId);
      await refreshFriends(); // Atualizar lista
    } catch (err: any) {
      console.error('Erro ao enviar solicitação:', err);
      setError(err.message || 'Erro ao enviar solicitação de amizade');
      throw err;
    }
  };

  const acceptFriendRequest = async (friendshipId: string) => {
    try {
      await FriendsAPI.acceptFriendRequest(friendshipId);
      await refreshFriends(); // Atualizar listas
    } catch (err: any) {
      console.error('Erro ao aceitar solicitação:', err);
      setError(err.message || 'Erro ao aceitar solicitação');
      throw err;
    }
  };

  const rejectFriendRequest = async (friendshipId: string) => {
    try {
      await FriendsAPI.rejectFriendRequest(friendshipId);
      await refreshFriends(); // Atualizar listas
    } catch (err: any) {
      console.error('Erro ao rejeitar solicitação:', err);
      setError(err.message || 'Erro ao rejeitar solicitação');
      throw err;
    }
  };

  const removeFriend = async (friendshipId: string) => {
    try {
      await FriendsAPI.removeFriend(friendshipId);
      await refreshFriends(); // Atualizar listas
    } catch (err: any) {
      console.error('Erro ao remover amigo:', err);
      setError(err.message || 'Erro ao remover amigo');
      throw err;
    }
  };

  // ===== AÇÕES DE RECOMENDAÇÃO =====

  const sendRecommendation = async (receiverId: string, gameId: string, message: string) => {
    try {
      await FriendsAPI.sendRecommendation(receiverId, gameId, message);
      // Não precisa atualizar listas, é uma ação de envio
    } catch (err: any) {
      console.error('Erro ao enviar recomendação:', err);
      setError(err.message || 'Erro ao enviar recomendação');
      throw err;
    }
  };

  const markRecommendationAsRead = async (recommendationId: string) => {
    try {
      await FriendsAPI.markRecommendationAsRead(recommendationId);
      // Atualizar recomendação local
      setRecommendations(prev => 
        prev.map(rec => 
          rec.id === recommendationId 
            ? { ...rec, is_read: true }
            : rec
        )
      );
    } catch (err: any) {
      console.error('Erro ao marcar recomendação como lida:', err);
      setError(err.message || 'Erro ao marcar como lida');
      throw err;
    }
  };

  // ===== BUSCA =====

  const searchUsers = async (query: string): Promise<Friend[]> => {
    try {
      return await FriendsAPI.searchUsers(query);
    } catch (err: any) {
      console.error('Erro ao buscar usuários:', err);
      setError(err.message || 'Erro ao buscar usuários');
      throw err;
    }
  };

  // ===== UTILITÁRIOS =====

  const getFriendshipStatus = async (userId: string): Promise<string | null> => {
    try {
      return await FriendsAPI.getFriendshipStatus(userId);
    } catch (err: any) {
      console.error('Erro ao verificar status da amizade:', err);
      return null;
    }
  };

  const isFriend = (userId: string): boolean => {
    return friends.some(friend => friend.id === userId);
  };

  // ===== EFEITOS =====

  // Carregar dados iniciais quando o usuário fizer login
  useEffect(() => {
    if (isAuthenticated && user) {
      setIsLoading(true);
      Promise.all([
        refreshFriends(),
        refreshActivities()
      ]).finally(() => {
        setIsLoading(false);
      });
    } else {
      // Limpar dados quando o usuário fizer logout
      setFriends([]);
      setOnlineFriends([]);
      setPendingRequests([]);
      setActivities([]);
      setRecommendations([]);
      setError(null);
    }
  }, [isAuthenticated, user]);

  // Atualizar amigos online periodicamente
  useEffect(() => {
    if (!isAuthenticated) return;

    const interval = setInterval(async () => {
      try {
        const onlineFriendsData = await FriendsAPI.getOnlineFriends();
        const filteredOnlineFriends = onlineFriendsData.filter(friend => friend.id !== user?.id);
        setOnlineFriends(filteredOnlineFriends);
      } catch (err) {
        console.error('Erro ao atualizar amigos online:', err);
      }
    }, 30000); // Atualizar a cada 30 segundos

    return () => clearInterval(interval);
  }, [isAuthenticated, user]);

  const value: FriendsContextType = {
    // Estado dos dados
    friends,
    onlineFriends,
    pendingRequests,
    activities,
    recommendations,
    
    // Estados de carregamento
    isLoading,
    isLoadingFriends,
    isLoadingActivities,
    
    // Erros
    error,
    
    // Ações
    refreshFriends,
    refreshActivities,
    sendFriendRequest,
    acceptFriendRequest,
    rejectFriendRequest,
    removeFriend,
    sendRecommendation,
    markRecommendationAsRead,
    searchUsers,
    
    // Utilitários
    getFriendshipStatus,
    isFriend,
  };

  return (
    <FriendsContext.Provider value={value}>
      {children}
    </FriendsContext.Provider>
  );
}

export function useFriends() {
  const context = useContext(FriendsContext);
  if (context === undefined) {
    throw new Error('useFriends must be used within a FriendsProvider');
  }
  return context;
}

export default FriendsContext;
