"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { LibraryService, Library, LibraryItem, UserStats } from './library-service';

interface LibraryContextType {
  library: Library | null;
  isLoading: boolean;
  error: string | null;
  userStats: UserStats | null;
  refreshLibrary: () => Promise<void>;
  toggleFavorite: (itemId: string, isFavorite: boolean) => Promise<void>;
  recordPlaytime: (itemId: string, minutes: number) => Promise<void>;
}

// Criar contexto com valor padrão
const LibraryContext = createContext<LibraryContextType | undefined>(undefined);

// Hook personalizado para usar o contexto
export function useLibrary() {
  const context = useContext(LibraryContext);
  if (context === undefined) {
    throw new Error('useLibrary deve ser usado dentro de um LibraryProvider');
  }
  return context;
}

// Provider component
export function LibraryProvider({ children }: { children: ReactNode }) {
  const [library, setLibrary] = useState<Library | null>(null);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Instância do serviço de biblioteca
  const libraryService = LibraryService.getInstance();

  // Carregar biblioteca do usuário ao montar o componente
  useEffect(() => {
    refreshLibrary();
  }, []);

  // Função para atualizar dados da biblioteca
  const refreshLibrary = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const libraryData = await libraryService.getLibrary();
      setLibrary(libraryData);
      
      // Obter estatísticas do usuário
      const stats = await libraryService.getUserStats();
      setUserStats(stats);
    } catch (err: any) {
      console.error('Erro ao carregar biblioteca:', err);
      setError(err.message || 'Erro ao carregar biblioteca');
    } finally {
      setIsLoading(false);
    }
  };

  // Alternar favorito
  const toggleFavorite = async (itemId: string, isFavorite: boolean) => {
    try {
      await libraryService.toggleFavorite(itemId, isFavorite);
      await refreshLibrary(); // Recarregar biblioteca para refletir as mudanças
    } catch (err: any) {
      console.error('Erro ao atualizar favorito:', err);
      setError(err.message || 'Erro ao atualizar favorito');
    }
  };

  // Registrar tempo de jogo
  const recordPlaytime = async (itemId: string, minutes: number) => {
    try {
      await libraryService.recordPlaytime(itemId, minutes);
      await refreshLibrary(); // Recarregar biblioteca para refletir as mudanças
    } catch (err: any) {
      console.error('Erro ao registrar tempo de jogo:', err);
      setError(err.message || 'Erro ao registrar tempo de jogo');
    }
  };

  // Valor do contexto
  const value = {
    library,
    isLoading,
    error,
    userStats,
    refreshLibrary,
    toggleFavorite,
    recordPlaytime
  };

  return (
    <LibraryContext.Provider value={value}>
      {children}
    </LibraryContext.Provider>
  );
}
