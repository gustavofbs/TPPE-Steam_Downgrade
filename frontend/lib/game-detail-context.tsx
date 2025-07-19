"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { CatalogService, Game, GameVersion } from './catalog-service';

interface GameDetailContextType {
  game: Game | null;
  versions: GameVersion[];
  isLoading: boolean;
  error: string | null;
  selectedVersion: GameVersion | null;
  setSelectedVersion: (version: GameVersion) => void;
  addToWishlist: (gameId: string) => Promise<void>;
  purchaseGame: (gameId: string, versionId: string) => Promise<void>;
}

// Criar contexto
const GameDetailContext = createContext<GameDetailContextType | undefined>(undefined);

// Hook personalizado
export function useGameDetail() {
  const context = useContext(GameDetailContext);
  if (context === undefined) {
    throw new Error('useGameDetail deve ser usado dentro de um GameDetailProvider');
  }
  return context;
}

// Provider component
export function GameDetailProvider({ children, slug }: { children: ReactNode; slug: string }) {
  const [game, setGame] = useState<Game | null>(null);
  const [versions, setVersions] = useState<GameVersion[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedVersion, setSelectedVersion] = useState<GameVersion | null>(null);
  
  // Instância do serviço
  const catalogService = CatalogService.getInstance();

  // Carregar detalhes do jogo
  useEffect(() => {
    console.log("Slug recebido no provider:", slug);
    const loadGameDetails = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // Obter detalhes do jogo
        const gameData = await catalogService.getGameDetails(slug);
        setGame(gameData);
        
        // Obter versões do jogo
        const versionsData = await catalogService.getGameVersions(gameData.slug);
        setVersions(versionsData);
        
        // Definir a versão padrão (primeira versão)
        if (versionsData.length > 0) {
          setSelectedVersion(versionsData[0]);
        }
      } catch (err: any) {
        console.error('Erro ao carregar detalhes do jogo:', err);
        setError(err.message || 'Erro ao carregar detalhes do jogo');
      } finally {
        setIsLoading(false);
      }
    };
    
    if (slug) {
      loadGameDetails();
    }
  }, [slug]);

  // Adicionar à lista de desejos
  const addToWishlist = async (gameId: string) => {
    try {
      await catalogService.addToWishlist(gameId);
    } catch (err: any) {
      console.error('Erro ao adicionar à lista de desejos:', err);
      throw err;
    }
  };

  // Comprar jogo
  const purchaseGame = async (gameId: string, versionId: string) => {
    try {
      await catalogService.purchaseGame(gameId, versionId);
    } catch (err: any) {
      console.error('Erro ao comprar jogo:', err);
      throw err;
    }
  };

  // Valor do contexto
  const value = {
    game,
    versions,
    isLoading,
    error,
    selectedVersion,
    setSelectedVersion,
    addToWishlist,
    purchaseGame
  };

  return (
    <GameDetailContext.Provider value={value}>
      {children}
    </GameDetailContext.Provider>
  );
}
